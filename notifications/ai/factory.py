from notifications.ai.token_budget_v1 import TokenBudget_v1
from notifications.ai.tokens import Tokens


class TokenBudgetFactory:
    @staticmethod
    def create_token_budget_v1(tokens=0):
        return TokenBudget_v1(Tokens(tokens))
