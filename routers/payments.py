from datetime import datetime
from typing import Union
from fastapi import APIRouter, Body

router = APIRouter()


@router.get("/payments")
async def get_payments(offset: int = 0, limit: int = 100):
    """
    List payments

        Args:
            offset (int, optional): number for "offset" entries
            limit (int, optional): number for "limit" entries         
        Returns:
            JSON with result
    """
    pass


@router.post("/payments/filter")
async def filter_payments(offset: int = 0, limit: int = 100):
    """
    List payments with filter

        Args:
            offset (int, optional): number for "offset" entries
            limit (int, optional): number for "limit" entries  
            payment_id (int, optional): id of payment
            booking_id (int, optional): id of booking that payment correspond to
            sum (float, optional): sum of payment
            date_from (datetime, optional): filter start time of the payment
            date_till (datetime, optional): filter end time of the payment            
        Returns:
            JSON with result
    """
    pass

@router.post("/payments")
async def create_payment():
    """
    Create payment

        Args:
            booking_id (int): id of booking that payment correspond to
            sum (float): sum of payment
            date (datetime): time of the payment
            description (str, optional): description of payment
        Returns:
            JSON with result
    """
    pass


@router.put("/payments/{payment_id}")
async def update_payment():
    """
    Update payment

        Args:
            payment_id (int): id of payment
            booking_id (int): id of booking that payment correspond to
            sum (float): sum of payment
            date (datetime): time of the payment
            description (str, optinal): description of payment
        Returns:
            JSON with result
    """
    pass


@router.delete("/payments/{payment_id}")
async def delete_payment():
    """
    Delete payment

        Args:
            payment_id (int): id of payment

        Returns:
            JSON with result
    """
    pass
