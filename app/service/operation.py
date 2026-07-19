from fastapi import HTTPException
from app.database import SessionLocal
from app.schemas import OperationRequest
from app.repository import wallets as wallets_repository
from sqlalchemy.orm import Session
def add_income(db: Session,operation: OperationRequest):
        if not wallets_repository.is_wallet_exist(db,operation.wallet_name):
            raise HTTPException(status_code=404, detail=f"Wallet'{operation.wallet_name}' not found") 
        #Добавляем  к балансу кошелька
        wallet = wallets_repository.add_income(db, operation.wallet_name, operation.amount)
        db.commit()
        #Возвразвем информацию об операции
        return {
            "message": "Income added",
            "wallet": operation.wallet_name,
            "ammount": operation.amount,
            "description": operation.description,
            "new_balance": wallet.balance
        }
    

def add_expense(db: Session,operation: OperationRequest):

        if not wallets_repository.is_wallet_exist(db,operation.wallet_name):
            raise HTTPException(status_code=404, detail=f"Wallet'{operation.wallet_name}' not found") 
        #Добавляем  к балансу кошелька
        wallet = wallets_repository.get_wallet_by_name(db,operation.wallet_name)
        if wallet.balance < operation.amount:
            raise HTTPException(status_code= 404, detail= f"Insufficient funds. Available: {wallet.balance}")
        wallet = wallets_repository.add_expence(db,operation.wallet_name, operation.amount)
        db.commit()
        #Возвразвем информацию об операции
        return {
                "message": "Expense added",
                "wallet": operation.wallet_name,
                "ammount": operation.amount,
                "description": operation.description,
                "new_balance": wallet.balance
            }
