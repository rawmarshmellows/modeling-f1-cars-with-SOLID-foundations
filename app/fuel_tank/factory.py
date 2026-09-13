from app.fuel_tank.fuel import Fuel
from app.fuel_tank.fuel_tank_v1 import FuelTank_v1


class FuelTankFactory:
    @staticmethod
    def create_fuel_tank_v1(fuel_amount_in_liters=140):
        return FuelTank_v1(Fuel.create_from_amount_in_liters(fuel_amount_in_liters))
