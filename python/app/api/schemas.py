from datetime import date
from pydantic import BaseModel, ConfigDict
from typing import List
from decimal import Decimal

class WithdrawalOut(BaseModel):
    id: int
    amount: Decimal
    date: date

    model_config = ConfigDict(from_attributes=True)

class TimeDepositOut(BaseModel):
    id: int
    planType: str
    balance: Decimal
    days: int
    withdrawals: List[WithdrawalOut]

    model_config = ConfigDict(from_attributes=True)