from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
#from pyde import BaseModel, Field
#инициализация FastApi
app = FastAPI() 

#Healtcheck 
#from fastapi.responses import Response #respons формирует ответ
#@app.get ("/health")
#def health_check():
#    return Response(status_code =200)

BALANCE = {}

class OperationRequest(BaseModel):
    wallet_name: str = Field(..., max_length= 127) #максимальное кол-во симвалов который может ввести пол
    amount: float
    description: str | None = Field(None, max_length= 255)
    
    @field_validator("amount")  #проверка суммы кошелька
    def amount_must_be_pos(cls, v: float) -> float:
        #Проверить что значение больше нуля
        if v <= 0:
            raise ValueError("Ammount must be positive")
        #Возвращаем если все OK
        return v 
    
    @field_validator("wallet_name") #проверка названия кошелька
    def wallet_name_not_empty(cls, v: str) -> str:
        #убираем пробелы
        v = v.strip()
        #проверяем что строка не пустая
        if not v:
            raise ValueError("WAllet name not empty")
        #возвращения значения
        return v

class CreateWalletRequest(BaseModel):
    name: str = Field(..., max_length= 127)
    initial_balance: float =0

    @field_validator("name") #проверка названия кошелька
    def name_not_empty(cls, v: str) -> str:
        #убираем пробелы
        v = v.strip()
        #проверяем что строка не пустая
        if not v:
            raise ValueError("WAllet name not empty")
        #возвращения значения
        return v

    @field_validator("initial_balance")  #проверка суммы кошелька
    def ballance_not_negative(cls, v: float) -> float:
        #Проверить что значение больше нуля
        if v < 0:
            raise ValueError("initial balance cannot be negative")
        #Возвращаем если все OK
        return v 

@app.get("/balance")
def get_balance(wallet_name: str | None = None): #get_balance название функиции, wallet_name: str | None = None - переменная типа строока со входящим параметром None
    # Если имя кошелька не указано- считаем общий баланс
    if wallet_name is None:
        return {"total_balance": sum(BALANCE.values())}
    # Проверяем существует запрошенный кошелек
    if wallet_name not in BALANCE:
        raise HTTPException (
            status_code = 404,
            detail = f"Wallet '{wallet_name}' not found"
        )
    # Возвращаем баланс конкретного кошелька
    return {"wallet_name": wallet_name, "balance": BALANCE[wallet_name]}

#path-параметр
@app.post("/wallet")
def create_wallet(wallet: CreateWalletRequest):
    #проверяем не существует ли такой кошелек
    if wallet.name in BALANCE:
        raise HTTPException(status_code=404, detail=f"Wallet '{wallet.name}' alredy exists")
    #создаем новый кошелек
    BALANCE[wallet.name] = wallet.initial_balance
    #возвращвем информацию о новом кошельке
    return {
        "message": f"Wallet'{wallet.name}' create",
        "wallet": wallet.name,
        "balance": BALANCE[wallet.name]
    }
@app.post("/operations/income")
def add_income(operation: OperationRequest):
    #Проверяем сущеустсвует кошелек
    if operation.wallet_name not in BALANCE:
        raise HTTPException(status_code=404, detail=f"Wallet'{operation.wallet_name}' not found") 
    #Добавляем  к балансу кошелька
    BALANCE[operation.wallet_name]+= operation.amount
    #Возвразвем информацию об операции
    return {
        "message": "Income added",
        "wallet": operation.wallet_name,
        "ammount": operation.amount,
        "description": operation.description,
        "new_balance": BALANCE[operation.wallet_name]
    }

@app.post("/operation/expense")
def add_expense(operation: OperationRequest):
    #Проверяем сущеустсвует кошелек
    if operation.wallet_name not in BALANCE:
        raise HTTPException(status_code=404, detail=f"Wallet'{operation.wallet_name}' not found")
    #Проверяем достаточно ли средств
    if BALANCE[operation.wallet_name] < operation.amount:
        raise HTTPException(status_code= 404, detail= f"Insufficient funds. Available: {BALANCE[operation.wallet_name]}")
    #Вычитаем расход из баланса кошелька
    BALANCE[operation.wallet_name] -= operation.amount
    #Возвразвем информацию об операции
    return {
        "message": "Expense added",
        "wallet": operation.wallet_name,
        "ammount": operation.amount,
        "description": operation.description,
        "new_balance": BALANCE[operation.wallet_name]
    }