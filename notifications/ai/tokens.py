class Tokens:
    """AI tokens. Making a message pop costs 120 of them."""

    def __init__(self, amount):
        self.amount = amount

    def __add__(self, other):
        return Tokens(self.amount + other.amount)

    def __sub__(self, other):
        return Tokens(self.amount - other.amount)
