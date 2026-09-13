from app.fuel_tank.exceptions import NotEnoughFuelError
from app.telemetry_system.exceptions import TelemetryNotEnabledError


class Driver_v2:
    """Written against F1CarInterface: its signatures and its docstrings."""

    def start_car(self, car):
        try:
            car.start_engine()
        except TelemetryNotEnabledError:
            print("Telemetry is off, enabling it and trying again...")
            car.enable_telemetry()
            car.start_engine()

    def accelerate_car(self, car, fuel_amount_in_milliliters):
        try:
            car.push_accelerator(fuel_amount_in_milliliters)
        except NotEnoughFuelError:
            print("Out of fuel, turning the engine off")
            car.stop_engine()
