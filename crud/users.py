from db import database
from models import users as users_model
from schemas import users as users_schema
from utils import users as users_util
import datetime
from sqlalchemy import and_
from fastapi import HTTPException, Depends, status



async def get_user_by_email(email: str):
    """ Get info about user """

    query = users_model.users_table.select().where(users_model.users_table.c.email == email)
    return await database.fetch_one(query)


async def get_user_by_token(token: str):
    """ Get info about token holder """

    query = users_model.tokens_table.join(users_model.users_table).select().where(
        and_(
            users_model.tokens_table.c.token == token,
            users_model.tokens_table.c.expires > datetime.datetime.now()
        )
    )
    return await database.fetch_one(query)


async def create_user_token(user_id: int):
    """ Create token for user """

    query = (
        users_model.tokens_table.insert()
        .values(expires=datetime.datetime.now() + datetime.timedelta(weeks=2), user_id=user_id)
        .returning(users_model.tokens_table.c.token, users_model.tokens_table.c.expires)
    )

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
    token = await create_user_token(user_id)
    token_dict = {"token": token["token"], "expires": token["expires"]}

    return {**user.dict(), "id": user_id, "is_active": True, "token": token_dict}


async def get_current_user(token: str = Depends(users_util.oauth2_scheme)):
    user = await get_user_by_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return user    