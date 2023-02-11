from ..engine.engine_1950s_2_5L_naturally_aspirated_v1 import Engine1950s_2_5L_NaturallyAspirated_v1
from ..chassis.chassis_v1 import Chassis_v1
from ..wheels.wheels_v1 import Wheels_v1
from ..fuel_tank.fuel_tank_v1 import FuelTank_v1

class F1Car_v1:
    def __init__(self):
        self.engine = self._construct_engine()
        self.chassis = self._construct_chassis()
        self.wheels = self._construct_wheels()
        self.fuel_tank = self._construct_fuel_tank()

    def _construct_engine(self):
        return Engine1950s_2_5L_NaturallyAspirated_v1()

    def _construct_chassis(self):
        return Chassis_v1()

    def _construct_wheels(self):
        return Wheels_v1()

    def _construct_fuel_tank(self):
        return FuelTank_v1()


    def push_accelerator(self, fuel_amount):
        self.engine.inject_air()
        fuel = self.fuel_tank.use_fuel(fuel_amount)
        self.engine.inject_fuel(fuel)

    def start_engine(self):
        self.engine.start()

    def stop_engine(self):
        self.engine.stop()
