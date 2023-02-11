from .exceptions import NotEnoughFuelError
from .fuel import Fuel

class FuelTank_v1:
    def __init__(self, current_fuel_in_tank=100):
        self.current_fuel_in_tank = current_fuel_in_tank

    def use_fuel(self, amount):
        amount_of_fuel_after_getting_fuel = self.current_fuel_in_tank.amount - amount
        if amount_of_fuel_after_getting_fuel < 0:
            raise NotEnoughFuelError("There is not enough fuel!")

        fuel = Fuel(amount)
        self.current_fuel_in_tank.amount -= fuel.amount
        return fuel


