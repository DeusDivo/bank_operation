from pydantic import BaseModel, Field, field_validator

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