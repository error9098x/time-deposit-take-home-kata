from datetime import date
from decimal import Decimal
from sqlalchemy.orm import Session
from app.infrastructure.database import Base, engine, SessionLocal
from app.infrastructure.models import TimeDepositModel, WithdrawalModel

def seed():
    Base.metadata.drop_all(bind=engine) # Start fresh
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        if db.query(TimeDepositModel).count() == 0:
            print("Seeding database...")
            t1 = TimeDepositModel(planType="basic", days=45, balance=Decimal("1234.56"))
            t2 = TimeDepositModel(planType="student", days=200, balance=Decimal("2000.00"))
            t3 = TimeDepositModel(planType="premium", days=50, balance=Decimal("5000.00"))

            db.add_all([t1, t2, t3])
            db.flush() # Flush to get IDs for foreign keys

            w1 = WithdrawalModel(timeDepositId=t1.id, amount=Decimal("12.34"), date=date(2025, 1, 15))
            w2 = WithdrawalModel(timeDepositId=t2.id, amount=Decimal("20.00"), date=date(2025, 2, 10))
            db.add_all([w1, w2])
            db.commit()
            print("Database seeded successfully.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()