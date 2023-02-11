from .electricity import Electricity
from .battery_v1 import Battery_v1

class BatteryFactory:
    @staticmethod
    def create_battery_v1(electricity_amount=0):
        return Battery_v1(current_electricity=Electricity(amount=electricity_amount))
