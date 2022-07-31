from typing import List
from fastapi import APIRouter
from schemas import requests as requests_schema

router = APIRouter()


@router.get("/requests", response_model=List[requests_schema.RequestInfo])
async def get_requests(offset: int = 0, limit: int = 100):
    """
    List requests

        Args:
            offset (int, optional): number for "offset" entries
            limit (int, optional): number for "limit" entries   
        Returns:
            response: RequestInfo
                JSON with result
    """
    pass


@router.post("/requests/filter", response_model=List[requests_schema.RequestInfo])
async def filter_requests(filter: requests_schema.RequestFilter, offset: int = 0, limit: int = 100):
    """
    List requests with filter

        Args:
            offset (int, optional): number for "offset" entries
            limit (int, optional): number for "limit" entries           

            filter: RequestFilter
                parameters required to filter requests
        Returns:
            response: RequestInfo
                JSON with result
    """
    pass


@router.post("/requests", response_model=requests_schema.RequestInfo)
async def create_request(request: requests_schema.RequestCreate):
    """
    Create request

        Args:
            request: RequestCreate
                parameters required to create a request
        Returns:
            response: RequestInfo
                JSON with result
    """
    pass


@router.put("/requests/{request_id}", response_model=requests_schema.RequestInfo)
async def update_request(request_id: int, request: requests_schema.RequestCreate):
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
    pass


@router.delete("/requests/{request_id}", response_model=requests_schema.DeleteInfo)
async def delete_request(request_id: int):
    """
    Delete request

        Args:
            request_id (int): id of request
        Returns:
            JSON with result
    """
    pass
