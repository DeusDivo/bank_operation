from pydantic import BaseModel, Field, field_validator
class Income(BaseModel):
    amount: int
    wallet: str | None = None
"""
data = {"amount": 500, "wallet":"cash" }
income = Income(**data)

income_dict = income.model_dump()

print(income_dict)
"""