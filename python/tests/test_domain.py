import unittest
from app.domain.models import TimeDeposit
from app.domain.services import TimeDepositCalculator


class TestTimeDepositCalculator(unittest.TestCase):

    def test_update_balance_basic_plan_after_30_days(self):
        deposits = [TimeDeposit(id=1, planType='basic', balance=1000.00, days=45)]
        calc = TimeDepositCalculator()
        calc.update_balance(deposits)
        # 1% APR monthly after 30 days: 1000 * 0.01 / 12 = 0.8333.. => rounded to 0.83, added once
        self.assertAlmostEqual(deposits[0].balance, 1000.83, places=2)

    def test_update_balance_student_plan_under_year(self):
        deposits = [TimeDeposit(id=1, planType='student', balance=1200.00, days=60)]
        calc = TimeDepositCalculator()
        calc.update_balance(deposits)
        # 3% APR monthly: 1200 * 0.03 / 12 = 3.0 => added once
        self.assertAlmostEqual(deposits[0].balance, 1203.00, places=2)

    def test_update_balance_premium_plan_after_45_days(self):
        deposits = [TimeDeposit(id=1, planType='premium', balance=2000.00, days=50)]
        calc = TimeDepositCalculator()
        calc.update_balance(deposits)
        # 5% APR monthly: 2000 * 0.05 / 12 = 8.333.. => 8.33 added once
        self.assertAlmostEqual(deposits[0].balance, 2008.33, places=2)