
class Electricity:
    """
    Electricity is a unit of energy. It is measured in watts.
    """
    @classmethod
    def create_from_amount_in_watts(cls, amount_in_watts):
        return cls(amount_in_watts)

    def __init__(self, amount):
        self._amount = amount
    
    @property    
    def amount_in_kilowatts(self):
        return self._amount / 1000
    
    @property    
    def amount_in_watts(self):
        return self._amount

    def __add__(self, other):
        return Electricity(self.amount_in_watts + other.amount_in_watts)

    def __sub__(self, other):
        return Electricity(self.amount_in_watts - other.amount_in_watts)


    

    
