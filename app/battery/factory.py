from app.battery.battery_v1 import Battery_v1
from app.battery.electricity import Electricity


class BatteryFactory:
    @staticmethod
    def create_battery_v1(charge_in_kilojoules=0):
        return Battery_v1(Electricity.create_from_amount_in_kilojoules(charge_in_kilojoules))
