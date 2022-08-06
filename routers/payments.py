from datetime import datetime
from typing import List, Union
from fastapi import APIRouter, Body
from schemas import payments as payments_schema
from crud import payments as payments_crud

router = APIRouter()


@router.post("/payments/filter", response_model=List[payments_schema.PaymentInfo])
async def filter_payments(filter: payments_schema.PaymentFilter, offset: int = 0, limit: int = 100):
    """
    List payments with filter

        Args:
            offset (int, optional): number for "offset" entries
            limit (int, optional): number for "limit" entries

            filter: PaymentFilter
                parameters required to filter
        Returns:
            response: List[PaymentInfo]
                JSON with result
    """
    return await payments_crud.filter_payments(filter=filter, offset=offset, limit=limit)


@router.post("/payments", response_model=payments_schema.PaymentInfo)
async def create_payment(payment: payments_schema.PaymentCreate):
    """
    Create payment

        Args:
            payment: PaymentCreate
                parameters required to create a payment
        Returns:
            response: PaymentInfo
                JSON with resulted instance
    """
    return await payments_crud.create_payment(payment=payment)


@router.put("/payments/{payment_id}", response_model=payments_schema.PaymentInfo)
async def update_payment(payment_id: int, payment: payments_schema.PaymentCreate):
    """
    Update payment

        Args:
            payment_id (int): id of payment

            payment: PaymentCreate
                parameters required to update a payment
        Returns:
            response: PaymentInfo
                JSON with resulted instance
    """
    return await payments_crud.update_payment(payment_id=payment_id, payment=payment)


@router.delete("/payments/{payment_id}", response_model=payments_schema.PaymentDeleteInfo)
async def delete_payment(payment_id: int):
    """
    Delete payment

        Args:
            payment_id (int): id of payment

        Returns:
            response: DeleteInfo
                JSON with result (Success, Error)
    """
    return await payments_crud.delete_payment(payment_id=payment_id)
