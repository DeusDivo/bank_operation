from fastapi import HTTPException
from app.database import SessionLocal
from app.repository import wallets as wallets_repository
from app.schemas import CreateWalletRequest
from decimal import Decimal
from sqlalchemy.orm import Session
def get_wallet(db: Session,wallet_name: str | None = None):
 # Если имя кошелька не указано- считаем общий баланс
        if wallet_name is None:
            wallets = wallets_repository.get_all_wallets(db)
            return {"total_balance": sum(wallet.balance for wallet in wallets)}
        # Проверяем существует запрошенный кошелек
        if not wallets_repository.is_wallet_exist(db, wallet_name):
            raise HTTPException (
                status_code = 404,
                detail = f"Wallet '{wallet_name}' not found"
            )
        # Возвращаем баланс конкретного кошелька
        wallet = wallets_repository.get_wallet_by_name(db,wallet_name)
        return {"wallet": wallet.name, "balance": wallet.balance}


def create_wallet(db: Session,wallet: CreateWalletRequest):

    #проверяем не существует ли такой кошелек
        if wallets_repository.is_wallet_exist(db,wallet.name):
            raise HTTPException(status_code=404, detail=f"Wallet '{wallet.name}' alredy exists")
        #создаем новый кошелек
        wallet = wallets_repository.create_wallet(db, wallet.name, wallet.initial_balance)
        db.commit()
        #возвращвем информацию о новом кошельке
        return {
            "message": f"Wallet'{wallet.name}' create",
            "wallet": wallet.name,
            "balance": wallet.balance
        }