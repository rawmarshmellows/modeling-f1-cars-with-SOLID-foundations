from .electricity import  Electricity
from .exceptions import NotEnoughPowerError

class Battery_v1:
    def __init__(self, current_electricity):
        self.current_electricity = current_electricity

    def use_electricity(self, amount):
        amount_of_electricty_after_getting_electricity = (
            self.current_electricity.amount - amount
        )
        if amount_of_electricty_after_getting_electricity < 0:
            raise NotEnoughPowerError("There is not enough electricity!")
        electricity = Electricity(amount)
        self.current_electricity.amount -= electricity.amount
        return electricity
    
    def charge_electricity(self, amount):
        self.current_electricity.amount += amount

