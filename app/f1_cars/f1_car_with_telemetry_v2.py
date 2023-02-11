from .interface import F1CarInterface
from ..fuel_tank.fuel import Fuel

class F1CarWithTelemetry_v2(F1CarInterface):
    def __init__(self, engine, chassis, wheels, fuel_tank, telemetry_system):
        self.engine = engine
        self.chassis = chassis
        self.wheels = wheels
        self.fuel_tank = fuel_tank
        self.telemetry_system = telemetry_system

    def push_accelerator(self, fuel_amount_in_milliliters):
        fuel = Fuel.create_from_amount_in_milliliters(fuel_amount_in_milliliters)
        self.engine.inject_air()
        self.fuel_tank.use_fuel(fuel)
        self.engine.inject_fuel(fuel)
        self.save_current_telemetry()

    def start_engine(self):
        self.engine.start()

    def stop_engine(self):
        self.engine.stop()

    def enable_telemetry(self):
        self.telemetry_system.enable()

    def disable_telemetry(self):
        self.telemetry_system.disable()

    def get_current_telemetry(self):
        return {
             "fuel": self.fuel_tank.current_fuel_in_tank.amount_in_liters
        }

    def get_telemetry_logs(self):
        return self.telemetry_system.logs

    def save_current_telemetry(self):
        current_telemetry = self.get_current_telemetry()
        self.telemetry_system.save(current_telemetry)