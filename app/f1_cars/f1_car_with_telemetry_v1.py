from app.f1_cars.engine_interface import EngineInterface
from app.f1_cars.interface import F1CarInterface
from app.fuel_tank.fuel import Fuel
from app.telemetry_system.exceptions import TelemetryNotEnabledError


class F1CarWithTelemetry_v1(F1CarInterface):
    def __init__(self, engine: EngineInterface, chassis, wheels, fuel_tank, telemetry_system):
        self.engine = engine
        self.chassis = chassis
        self.wheels = wheels
        self.fuel_tank = fuel_tank
        self.telemetry_system = telemetry_system

    def start_engine(self):
        if not self.telemetry_system.is_enabled:
            raise TelemetryNotEnabledError("Enable telemetry before starting the engine!")
        self.engine.start()

    def stop_engine(self):
        self.engine.stop()

    def push_accelerator(self, fuel_amount_in_milliliters):
        fuel = Fuel.create_from_amount_in_milliliters(fuel_amount_in_milliliters)
        self.engine.inject_air()
        self.fuel_tank.use_fuel(fuel)
        self.engine.inject_fuel(fuel)
        self.telemetry_system.save(self.get_current_telemetry())

    def enable_telemetry(self):
        self.telemetry_system.enable()

    def disable_telemetry(self):
        self.stop_engine()
        self.telemetry_system.disable()

    def get_current_telemetry(self):
        return {"fuel_in_milliliters": self.fuel_tank.current_fuel_in_tank.amount_in_milliliters}

    def get_telemetry_logs(self):
        return list(self.telemetry_system.logs)
