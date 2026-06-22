from fastapi import APIRouter, HTTPException
from app.schemas import OperationRequest
from app.service import operation as operation_service

router = APIRouter()

@router.post("/operations/income")
def add_income(operation: OperationRequest):
   return operation_service.add_income(operation)

@router.post("/operation/expense")
def add_expense(operation: OperationRequest):
   return operation_service.add_expense(operation)