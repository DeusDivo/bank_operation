from fastapi import APIRouter
from app.service import wallets as wallets_service
from app.schemas import CreateWalletRequest
from app.dependency import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
router = APIRouter()

@router.get("/balance")
def get_balance(wallet_name: str | None = None, db: Session = Depends(get_db)): #get_balance название функиции, wallet_name: str | None = None - переменная типа строока со входящим параметром None
   return wallets_service.get_wallet(db,wallet_name)

#path-параметр
@router.post("/wallet")
def create_wallet(wallet: CreateWalletRequest, db: Session = Depends(get_db)):
    return wallets_service.create_wallet(db,wallet)