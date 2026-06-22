from fastapi import APIRouter
from app.service import wallets as wallets_service
from app.schemas import CreateWalletRequest
router = APIRouter()

@router.get("/balance")
def get_balance(wallet_name: str | None = None): #get_balance название функиции, wallet_name: str | None = None - переменная типа строока со входящим параметром None
   return wallets_service.get_wallet(wallet_name)

#path-параметр
@router.post("/wallet")
def create_wallet(wallet: CreateWalletRequest):
    return wallets_service.create_wallet(wallet)