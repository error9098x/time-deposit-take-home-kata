from datetime import date
from decimal import Decimal
from sqlalchemy import Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.database import Base

class TimeDepositModel(Base):
    __tablename__ = "time_deposits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    planType: Mapped[str] = mapped_column(String, nullable=False)
    days: Mapped[int] = mapped_column(Integer, nullable=False)
    balance: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)

    withdrawals: Mapped[list["WithdrawalModel"]] = relationship(
        back_populates="time_deposit", cascade="all, delete-orphan", lazy="selectin"
    )

class WithdrawalModel(Base):
    __tablename__ = "withdrawals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timeDepositId: Mapped[int] = mapped_column(ForeignKey("time_deposits.id"), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)

    time_deposit: Mapped[TimeDepositModel] = relationship(back_populates="withdrawals")