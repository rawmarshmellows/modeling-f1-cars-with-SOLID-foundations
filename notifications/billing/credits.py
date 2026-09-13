class Credits:
    """Message credits. One credit pays for one 160-character SMS segment."""

    def __init__(self, amount):
        self.amount = amount

    def __add__(self, other):
        return Credits(self.amount + other.amount)

    def __sub__(self, other):
        return Credits(self.amount - other.amount)
