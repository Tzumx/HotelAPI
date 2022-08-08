from db import database
from models import users as users_model
from schemas import users as users_schema
from utils import users as users_util
from fastapi import HTTPException


async def get_user_by_email(email: str):
    """ Get info about user """

    query = users_model.users_table.select().where(
        users_model.users_table.c.email == email)
    return await database.fetch_one(query)


async def create_user(user: users_schema.UserCreate):
    """ Create new user """

    db_user = await get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    salt = users_util.get_random_string()
    hashed_password = users_util.hash_password(user.password, salt)
    query = users_model.users_table.insert().values(
        email=user.email, name=user.name, hashed_password=f"{salt}${hashed_password}"
    )
    user_id = await database.execute(query)
    token, expire = users_util.create_access_token(user.email)
    token_dict = {"token": token, "expires": expire}

    return {**user.dict(), "id": user_id, "is_active": True, "token": token_dict}
