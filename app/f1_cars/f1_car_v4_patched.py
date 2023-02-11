from ..engine.engine_1950s_2_5L_naturally_aspirated_v1 import Engine1950s_2_5L_NaturallyAspirated_v1
from ..engine.engine_1950s_2_5L_naturally_aspirated_v2 import Engine1950s_2_5L_NaturallyAspirated_v2
from ..engine.engine_1980s_1_5L_turbocharged_v1 import Engine1980s_1_5L_TurboCharged_v1
from ..fuel_tank.fuel import Fuel

class F1Car_v4_patched:
    def __init__(self, engine, chassis, wheels, fuel_tank):
        self.engine = engine
        self.chassis = chassis
        self.wheels = wheels
        self.fuel_tank = fuel_tank

    def push_accelerator(self, fuel_amount_in_milliliters):
        fuel = Fuel.create_from_amount_in_milliliters(fuel_amount_in_milliliters)
        self.engine.inject_air()
        self.fuel_tank.use_fuel(fuel)
        self.engine.inject_fuel(fuel)

    def start_engine(self):
        engine_type = type(self.engine)
        if engine_type == Engine1950s_2_5L_NaturallyAspirated_v1 or engine_type == Engine1950s_2_5L_NaturallyAspirated_v2:
            self.engine.start()
        if engine_type == Engine1980s_1_5L_TurboCharged_v1:
            self.engine.start_with_turbocharger()

    def stop_engine(self):
        self.engine.stop()
