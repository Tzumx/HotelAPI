from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from schemas import users as users_schema
from crud import users as users_crud
from utils import users as users_util

router = APIRouter()


@router.post("/sign-up", response_model=users_schema.User)
async def create_user(user: users_schema.UserCreate):
    """
    Create user

        Args:
            user: UserCreate
                parameters required to create a user
        Returns:
            response: User
                instance of created user
    """

    return await users_crud.create_user(user=user)


@router.post("/auth", response_model=users_schema.TokenBase)
async def auth(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login user

        Args:
            form_data: OAuth2PasswordRequestForm
                parameters required to login a user
        Returns:
            response: User
                instance of logged user's token
    """

    user = await users_crud.get_user_by_email(email=form_data.username)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not users_util.validate_password(
        password=form_data.password, hashed_password=user["hashed_password"]
    ):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    return await users_crud.create_user_token(user_id=user["id"])