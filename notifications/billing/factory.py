from notifications.billing.credit_balance_v1 import CreditBalance_v1
from notifications.billing.credits import Credits


class CreditBalanceFactory:
    @staticmethod
    def create_credit_balance_v1(credits=1_000):
        return CreditBalance_v1(Credits(credits))
