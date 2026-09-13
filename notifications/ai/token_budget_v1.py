from notifications.ai.exceptions import OutOfTokensError


class TokenBudget_v1:
    def __init__(self, tokens):
        self.tokens = tokens

    def can_afford(self, tokens):
        return tokens.amount <= self.tokens.amount

    def spend(self, tokens):
        if not self.can_afford(tokens):
            raise OutOfTokensError(f"Out of AI tokens! {tokens.amount} needed but only {self.tokens.amount} left")
        self.tokens -= tokens
