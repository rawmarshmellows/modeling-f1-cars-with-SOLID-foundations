from .exceptions import NotEnoughFuelError
from .fuel import Fuel

class FuelTank_v1:
    def __init__(self, current_fuel_in_tank=140):
        self.current_fuel_in_tank = current_fuel_in_tank

    def use_fuel(self, fuel):
        amount_of_fuel_after_getting_fuel = (self.current_fuel_in_tank - fuel).amount_in_liters

        if amount_of_fuel_after_getting_fuel < 0:
            raise NotEnoughFuelError(f"There is not enough fuel! {fuel.amount_in_liters}L requested but only {self.current_fuel_in_tank.amount_in_liters}L available")
        self.current_fuel_in_tank -= fuel


