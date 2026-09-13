class Electricity:
    """An amount of electrical energy, stored in kilojoules."""

    @classmethod
    def create_from_amount_in_kilojoules(cls, amount_in_kilojoules):
        return cls(amount_in_kilojoules)

    def __init__(self, amount_in_kilojoules):
        self._amount_in_kilojoules = amount_in_kilojoules

    @property
    def amount_in_kilojoules(self):
        return self._amount_in_kilojoules

    @property
    def amount_in_megajoules(self):
        return self._amount_in_kilojoules / 1000

    def __add__(self, other):
        return Electricity(self.amount_in_kilojoules + other.amount_in_kilojoules)

    def __sub__(self, other):
        return Electricity(self.amount_in_kilojoules - other.amount_in_kilojoules)
