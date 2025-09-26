from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.infrastructure.repositories import TimeDepositRepository
from app.application.services import TimeDepositService
from fastapi import Depends

def get_repository(db: Session = Depends(get_db)) -> TimeDepositRepository:
    return TimeDepositRepository(db=db)

def get_time_deposit_service(
    repository: TimeDepositRepository = Depends(get_repository),
    db: Session = Depends(get_db)
) -> TimeDepositService:
    return TimeDepositService(repository=repository, db=db)