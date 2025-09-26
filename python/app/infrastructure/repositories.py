from decimal import Decimal, ROUND_HALF_UP
from typing import List
from sqlalchemy.orm import Session, selectinload
from app.application.ports import TimeDepositDTO, TimeDepositRepositoryPort
from app.infrastructure.models import TimeDepositModel

class TimeDepositRepository(TimeDepositRepositoryPort):
    def __init__(self, db: Session):
        self._db = db

    def get_all(self) -> List[TimeDepositModel]:
        return (
            self._db.query(TimeDepositModel)
            .options(selectinload(TimeDepositModel.withdrawals))
            .order_by(TimeDepositModel.id)
            .all()
        )

    # Adapter method for application port to avoid leaking ORM to application layer
    def get_all_for_update(self) -> List[TimeDepositDTO]:
        rows = (
            self._db.query(TimeDepositModel)
            .order_by(TimeDepositModel.id)
            .all()
        )
        return [
            TimeDepositDTO(
                id=r.id,
                planType=r.planType,
                balance=float(r.balance),
                days=r.days,
            )
            for r in rows
        ]

    def save_updated_balances(self, items: List[TimeDepositDTO]) -> None:
        id_to_domain_map = {d.id: d for d in items}
        
        # Fetch the corresponding SQLAlchemy models to update
        db_models = self._db.query(TimeDepositModel).filter(
            TimeDepositModel.id.in_(id_to_domain_map.keys())
        ).all()

        for db_model in db_models:
            updated_domain_model = id_to_domain_map[db_model.id]
            # Convert float from domain model back to a safe Decimal for persistence
            db_model.balance = Decimal(str(updated_domain_model.balance)).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )