class Fuel:
    """
    This represents fuel in the unit of Liters
    """
    @classmethod
    def create_from_amount_in_liters(cls, amount_in_liters):
        return cls(amount_in_liters)

    @classmethod
    def create_from_amount_in_milliliters(cls, amount_in_milliliters):
        return cls(amount_in_milliliters / 1000)

    def __init__(self, amount):
        self._amount = amount

    @property
    def amount_in_liters(self):
        return self._amount
    
    @property
    def amount_in_milliliters(self):
        return self._amount * 1000

    def __add__(self, other):
        return Fuel(self.amount_in_liters + other.amount_in_liters)

    def __sub__(self, other):
        return Fuel(self.amount_in_liters - other.amount_in_liters)
