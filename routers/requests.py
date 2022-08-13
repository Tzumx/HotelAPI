from typing import List

from fastapi import APIRouter, Depends

from crud import requests as requests_crud
from schemas import requests as requests_schema
from schemas import users as users_schema
from utils import users as users_utils

router = APIRouter()


@router.post("/requests/filter", response_model=List[requests_schema.RequestInfo],
             tags=["requests"])
async def filter_requests(filter: requests_schema.RequestFilter = requests_schema.RequestFilter(**{}),
                          offset: int = 0, limit: int = 100,
                          user: users_schema.User = Depends(users_utils.get_current_user)):
    """
    List requests with filter

        Args:
            offset (int, optional): number for "offset" entries
            limit (int, optional): number for "limit" entries

            filter: RequestFilter
                parameters required to filter requests
        Returns:
            response: List[RequestInfo]
                JSON with result
    """
    return await requests_crud.filter_requests(filter=filter, offset=offset, limit=limit)


@router.post("/requests", response_model=requests_schema.RequestInfo,
             tags=["requests"])
async def create_request(request: requests_schema.RequestCreate,
                         user: users_schema.User = Depends(users_utils.get_current_user)):
    """
    Create request

        Args:
            request: RequestCreate
                parameters required to create a request
        Returns:
            response: RequestInfo
                JSON with result
    """
    return await requests_crud.create_request(request=request)


@router.put("/requests/{request_id}", response_model=requests_schema.RequestUpdate,
            tags=["requests"])
async def update_request(request_id: int, request: requests_schema.RequestUpdate,
                         user: users_schema.User = Depends(users_utils.get_current_user)):
    """
    Update request

        Args:
            request_id (int): id of request

            request: RequestCreate
                parameters required to update a request
        Returns:
            response: RequestInfo
                JSON with result
    """
    return await requests_crud.update_request(request_id=request_id, request=request)


@router.delete("/requests/{request_id}", response_model=requests_schema.RequestDeleteInfo,
               tags=["requests"])
async def delete_request(request_id: int,
                         user: users_schema.User = Depends(users_utils.get_current_user)):
    """
    Delete request

        Args:
            request_id (int): id of request
        Returns:
            response: DeleteInfo
                JSON with result (Success, Error)
    """
    return await requests_crud.delete_request(request_id=request_id)
