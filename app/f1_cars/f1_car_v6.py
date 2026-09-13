from app.f1_cars.engine_interface import EngineInterface
from app.f1_cars.interface import F1CarInterface
from app.fuel_tank.fuel import Fuel


class F1Car_v6(F1CarInterface):
    """A 1950s car squeezed into F1CarInterface for the heritage demo day."""

    def __init__(self, engine: EngineInterface, chassis, wheels, fuel_tank):
        self.engine = engine
        self.chassis = chassis
        self.wheels = wheels
        self.fuel_tank = fuel_tank

    def start_engine(self):
        # Can't keep the invariant: there's no telemetry to record with
        self.engine.start()

    def stop_engine(self):
        self.engine.stop()

    def push_accelerator(self, fuel_amount_in_milliliters):
        fuel = Fuel.create_from_amount_in_milliliters(fuel_amount_in_milliliters)
        self.engine.inject_air()
        self.fuel_tank.use_fuel(fuel)
        self.engine.inject_fuel(fuel)

    # A 1950s car has no telemetry, but F1CarInterface insists on it
    def enable_telemetry(self):
        pass  # nothing to switch on

    def disable_telemetry(self):
        pass  # nothing to switch off

    def get_current_telemetry(self):
        return {}  # no sensors, so the "always includes fuel_in_milliliters" promise is broken

    def get_telemetry_logs(self):
        return []  # looks exactly like "the driver forgot to enable telemetry"
