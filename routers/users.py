from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from crud import users as users_crud
from schemas import users as users_schema
from utils import users as users_util

router = APIRouter()


@router.post("/sign-up", response_model=users_schema.UserOut)
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


@router.post("/auth", response_model=users_schema.TokenSchema)
async def auth(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login user

        Args:
            form_data: OAuth2PasswordRequestForm
                parameters required to login a user
        Returns:
            Dict of tokens
    """

    user = await users_crud.get_user_by_email(email=form_data.username)

    if not user:
        raise HTTPException(
            status_code=401, detail="Incorrect email or password")

    if not users_util.validate_password(
        password=form_data.password, hashed_password=user["hashed_password"]
    ):
        raise HTTPException(
            status_code=401, detail="Incorrect email or password")

    access_token, _ = users_util.create_access_token(
        subject=form_data.username)
    refresh_token, _ = users_util.create_refresh_token(
        subject=form_data.username)
    return {"access_token": access_token,
            "refresh_token": refresh_token}