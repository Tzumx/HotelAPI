from fastapi import HTTPException

from db import database
from models import users as users_model
from schemas import users as users_schema
from utils import users as users_util
from typing import Optional


async def get_user_by_email(email: str):
    """ Get info about user """

    query = users_model.user.select().where(
        users_model.user.c.email == email)
    return await database.fetch_one(query)


async def create_user(user: users_schema.UserCreate):
    """ Create new user """

    db_user = await get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    query = users_model.user.select()
    stored_data = await database.fetch_one(query)
    if stored_data == None: is_admin = True
    else: is_admin = False

    salt = users_util.get_random_string()
    hashed_password = users_util.hash_password(user.password, salt)
    query = users_model.user.insert().values(
        email=user.email, name=user.name, hashed_password=f"{salt}${hashed_password}",
        is_admin=is_admin
    )
    user_id = await database.execute(query)
    token, expire = users_util.create_access_token(user.email)
    token_dict = {"token": token, "expires": expire}

    return {**user.dict(), "id": user_id, "is_admin": is_admin, "is_active": True, "token": token_dict}


async def filter_users(filter: users_schema.UserFilter, offset: int = 0, limit: int = 100):
    """ Filter and get info about all users """

    query = users_model.user.select()
    filter_params = filter.dict(exclude_unset=True)
    for k, v in filter_params.items():
        query = query.where(users_model.user.c[k] == v)
    results = await database.fetch_all(query.order_by(users_model.user.c.id))
    return [dict(result._mapping) for result in results]


async def update_user(id: int, user: users_schema.UserUpdate):
    """ Update user """

    query = users_model.user.select().where(users_model.user.c.id == id)
    stored_data = await database.fetch_one(query)
    if stored_data != None:
        stored_data = dict(stored_data)
        update_data = user.dict(exclude_unset=True)
        if 'password' in update_data.keys():
            salt = users_util.get_random_string()
            hashed_password = users_util.hash_password(update_data['password'], salt)
            hashed_password = f"{salt}${hashed_password}"
            update_data.pop("password")
            update_data["hashed_password"] = hashed_password
        stored_data.update(update_data)
        query = users_model.user.update().values(**stored_data).where(
            users_model.user.c.id == id)
        await database.execute(query)
        return {**stored_data, "id": id}
    else:
        raise HTTPException(status_code=404, detail="Not found")


async def delete_user(id: int):
    """ Delete user by id """

    query = users_model.user.select().where(users_model.user.c.id == id)
    answer = await database.execute(query)
    if answer == id:
        query = users_model.user.delete().where(
            users_model.user.c.id == id)
        await database.execute(query)
        answer = "Success"
    else:
        answer = "Error"
        raise HTTPException(status_code=404, detail="Not found")
    return {"result": answer}
