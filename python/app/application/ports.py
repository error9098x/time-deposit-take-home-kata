from dataclasses import dataclass
from typing import List, Protocol


@dataclass
class TimeDepositDTO:
    id: int
    planType: str
    balance: float
    days: int


class TimeDepositRepositoryPort(Protocol):
    def get_all_for_update(self) -> List[TimeDepositDTO]:
        ...

    def save_updated_balances(self, items: List[TimeDepositDTO]) -> None:
        ...

