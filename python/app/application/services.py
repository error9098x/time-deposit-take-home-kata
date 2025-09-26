from typing import List
from sqlalchemy.orm import Session
from app.application.ports import TimeDepositRepositoryPort, TimeDepositDTO
from app.domain.models import TimeDeposit
from app.domain.services import TimeDepositCalculator


def map_to_domain(dtos: List[TimeDepositDTO]) -> List[TimeDeposit]:
    return [
        TimeDeposit(
            id=dto.id,
            planType=dto.planType,
            balance=dto.balance,
            days=dto.days,
        )
        for dto in dtos
    ]


class TimeDepositService:
    def __init__(self, repository: TimeDepositRepositoryPort, db: Session):
        self._repository = repository
        self._db = db
        self._calculator = TimeDepositCalculator()

    def update_all_balances(self) -> List[TimeDepositDTO]:
        with self._db.begin():
            items = self._repository.get_all_for_update()
            if not items:
                return []

            domain_models = map_to_domain(items)
            self._calculator.update_balance(domain_models)

            updated = [
                TimeDepositDTO(
                    id=d.id,
                    planType=d.planType,
                    balance=d.balance,
                    days=d.days,
                )
                for d in domain_models
            ]
            self._repository.save_updated_balances(updated)

        # fresh snapshot after commit for response
        return self._repository.get_all_for_update()