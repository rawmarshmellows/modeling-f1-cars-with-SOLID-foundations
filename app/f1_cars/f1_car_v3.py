from ..engine import EngineFactory
from ..chassis import ChassisFactory
from ..wheels import WheelsFactory
from ..fuel_tank import FuelTankFactory

class F1Car_v3:
    def __init__(self):
        self.engine = EngineFactory.create_engine_1950s_2_5L_naturally_aspirated_v2()
        self.chassis = ChassisFactory.create_chassis_v1()
        self.wheels = WheelsFactory.create_wheels_v1()
        self.fuel_tank = FuelTankFactory.create_fuel_tank_v1()

    def push_accelerator(self, fuel_amount):
        self.engine.inject_air()
        fuel = self.fuel_tank.use_fuel(fuel_amount)
        self.engine.inject_fuel(fuel)

    def start_engine(self):
        self.engine.start()

    def stop_engine(self):
        self.engine.stop()
