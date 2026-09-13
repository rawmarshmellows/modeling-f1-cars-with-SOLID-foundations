from notifications.billing.exceptions import NotEnoughCreditsError


class CreditBalance_v1:
    def __init__(self, credits):
        self.credits = credits

    def charge(self, credits):
        if credits.amount > self.credits.amount:
            raise NotEnoughCreditsError(
                f"Not enough credits! {credits.amount} needed but only {self.credits.amount} left"
            )
        self.credits -= credits
