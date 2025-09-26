from typing import List
from fastapi import APIRouter, Depends
from app.api.schemas import TimeDepositOut
from app.api.dependencies import get_time_deposit_service, get_repository
from app.application.services import TimeDepositService
from app.infrastructure.repositories import TimeDepositRepository

router = APIRouter()

@router.get("/")
def health_check():
    return {"status": "ok", "message": "Time Deposit Kata API is running"}

@router.get("/time-deposits", response_model=List[TimeDepositOut])
def get_all_time_deposits(repository: TimeDepositRepository = Depends(get_repository)):
    # Use repository directly for read with eager loading of withdrawals
    return repository.get_all()

@router.post("/time-deposits/update-balances", response_model=List[TimeDepositOut])
def update_balances(service: TimeDepositService = Depends(get_time_deposit_service)):
    return service.update_all_balances()