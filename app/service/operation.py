from fastapi import HTTPException
from app.schemas import OperationRequest
from app.repository import wallets as wallets_repository

def add_income(operation: OperationRequest):
    if not wallets_repository.is_wallet_exist(operation.wallet_name):
        raise HTTPException(status_code=404, detail=f"Wallet'{operation.wallet_name}' not found") 
    #Добавляем  к балансу кошелька
    new_balancy = wallets_repository.add_income(operation.wallet_name, operation.amount)
    #Возвразвем информацию об операции
    return {
        "message": "Income added",
        "wallet": operation.wallet_name,
        "ammount": operation.amount,
        "description": operation.description,
        "new_balance": new_balancy
    }

def add_expense(operation: OperationRequest):
    if not wallets_repository.is_wallet_exist(operation.wallet_name):
        raise HTTPException(status_code=404, detail=f"Wallet'{operation.wallet_name}' not found") 
    #Добавляем  к балансу кошелька
    balance = wallets_repository.get_wallet_by_name(operation.wallet_name)
    if balance < operation.amount:
        raise HTTPException(status_code= 404, detail= f"Insufficient funds. Available: {balance}")
    new_balance = wallets_repository.add_expence(operation.wallet_name, operation.amount)
    #Возвразвем информацию об операции
    return {
            "message": "Income added",
            "wallet": operation.wallet_name,
            "ammount": operation.amount,
            "description": operation.description,
            "new_balance": new_balance
        }
