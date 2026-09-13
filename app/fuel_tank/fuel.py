class Fuel:
    """An amount of fuel, stored in milliliters."""

    @classmethod
    def create_from_amount_in_liters(cls, amount_in_liters):
        return cls(amount_in_liters * 1000)

    @classmethod
    def create_from_amount_in_milliliters(cls, amount_in_milliliters):
        return cls(amount_in_milliliters)

    def __init__(self, amount_in_milliliters):
        self._amount_in_milliliters = amount_in_milliliters

    @property
    def amount_in_liters(self):
        return self._amount_in_milliliters / 1000

    @property
    def amount_in_milliliters(self):
        return self._amount_in_milliliters

    def __add__(self, other):
        return Fuel(self.amount_in_milliliters + other.amount_in_milliliters)

    def __sub__(self, other):
        return Fuel(self.amount_in_milliliters - other.amount_in_milliliters)
