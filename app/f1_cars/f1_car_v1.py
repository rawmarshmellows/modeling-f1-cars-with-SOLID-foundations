from ..engine.engine_1950s_1_5L_supercharged_v1 import Engine1950s_1_5L_Supercharged_v1
from ..chassis.chassis_spaceframe_v1 import Chassis_Spaceframe_v1
from ..wheels.wheels_v1 import Wheels_v1
from ..fuel_tank.fuel_tank_v1 import FuelTank_v1
from ..fuel_tank.fuel import Fuel

class F1Car_v1:
    def __init__(self):
        self.engine = self._construct_engine()
        self.chassis = self._construct_chassis()
        self.wheels = self._construct_wheels()
        self.fuel_tank = self._construct_fuel_tank()

    def _construct_engine(self):
        return Engine1950s_1_5L_Supercharged_v1()

    def _construct_chassis(self):
        return Chassis_Spaceframe_v1()

    def _construct_wheels(self):
        return Wheels_v1()

    def _construct_fuel_tank(self):
        return FuelTank_v1()


    def push_accelerator(self, fuel_amount_in_milliliters):
        fuel = Fuel.create_from_amount_in_milliliters(fuel_amount_in_milliliters)
        self.engine.inject_air()
        self.fuel_tank.use_fuel(fuel)
        self.engine.inject_fuel(fuel)

    def start_engine(self):
        self.engine.start()

    def stop_engine(self):
        self.engine.stop()
