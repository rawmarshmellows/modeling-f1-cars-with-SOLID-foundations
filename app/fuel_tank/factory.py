from .fuel_tank_v1 import FuelTank_v1
from .fuel import Fuel

class FuelTankFactory:
    @staticmethod
    def create_fuel_tank_v1(fuel_amount=100):
        return FuelTank_v1(Fuel(fuel_amount))