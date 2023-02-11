from .interface import NonHybridAccelerableInterface, StartableInterface

class F1Car_v5(NonHybridAccelerableInterface, StartableInterface):
    def __init__(self, engine, chassis, wheels, fuel_tank):
        self.engine = engine
        self.chassis = chassis
        self.wheels = wheels
        self.fuel_tank = fuel_tank

    def push_accelerator(self, fuel_amount):
        self.engine.inject_air()
        fuel = self.fuel_tank.use_fuel(fuel_amount)
        self.engine.inject_fuel(fuel)

    def start_engine(self):
        self.engine.start()

    def stop_engine(self):
        self.engine.stop()
