from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_jwt_auth import AuthJWT

from crud import users as users_crud
from schemas import users as users_schema
from utils import users as users_util

router = APIRouter()


@router.post("/sign-up", response_model=users_schema.UserInfo,
             summary="Register new user", tags=["users"])
async def create_user(user: users_schema.UserCreate,
                      user_admin: users_schema.User = Depends(users_util.get_admin_user)):
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


@router.post("/auth", response_model=users_schema.TokenSchema,
             summary="LogIn and get tokens", tags=["users"])
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


@router.post("/users/filter", response_model=List[users_schema.UserInfo],
             summary="Filter users", tags=["users"])
async def filter_users(filter: users_schema.UserFilter = users_schema.UserFilter(**{}),
                       offset: int = 0, limit: int = 100,
                       user: users_schema.User = Depends(users_util.get_admin_user)):
    """
    Get all users

        Args:
            offset (int, optional): number for "offset" entries
            limit (int, optional): number for "limit" entries

            room: UserFilter
                parameters required to filter users
        Returns:
            response: List[UserOut]
                JSON with users
    """

    return await users_crud.filter_users(filter=filter, offset=offset, limit=limit)


@router.put("/users/{id}", response_model=users_schema.UserInfo,
            summary="Update user", tags=["users"])
async def update_user(id: int, user_to_update: users_schema.UserUpdate,
                      user: users_schema.User = Depends(users_util.get_admin_user)):
    """
    Update info about the user

        Args:
            id (int): user id

            room: UserUpdate
                parameters required to update a user
        Returns:
            response: UserOut
                JSON with updated room instance
    """
    return await users_crud.update_user(id=id, user=user_to_update)


@router.delete("/users/{id}", response_model=users_schema.UserDeleteInfo,
               summary="Delete user", tags=["users"])
async def delete_user(id: int,
                      user: users_schema.User = Depends(users_util.get_admin_user)):
    """
    Delete user.

        Args:
                id (int): Id of entry to delete
        Returns:
                response: UserDeleteInfo
                    JSON with result of delete: Success or Error
    """
    return await users_crud.delete_user(id=id)


@router.post("/auth/refresh", response_model=users_schema.TokenRefreshSchema,
             summary="Refresh token for access", tags=["users"])
async def refresh_token(token=Depends(users_util.refresh_token)):
    """
    Refresh token for user

        Returns:
                response: Dict with access token
    """
    return token
