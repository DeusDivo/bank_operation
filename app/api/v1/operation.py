from fastapi import APIRouter, HTTPException
from app.dependency import get_db
from app.schemas import OperationRequest
from app.service import operation as operation_service
from sqlalchemy.orm import Session 
from fastapi import Depends
router = APIRouter()

@router.post("/operations/income")
def add_income(operation: OperationRequest, db: Session = Depends(get_db)):
   return operation_service.add_income(db,operation)

@router.post("/operation/expense")
def add_expense(operation: OperationRequest, db: Session = Depends(get_db)):
   return operation_service.add_expense(db,operation)