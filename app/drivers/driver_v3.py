from app.f1_cars.hybrid_f1_car_v2 import HybridF1Car_v2
from app.fuel_tank.exceptions import NotEnoughFuelError
from app.telemetry_system.exceptions import TelemetryNotEnabledError


class Driver_v3:
    """One driver for the whole heritage demo day, so it has to know about every car."""

    def start_car(self, car):
        try:
            car.start_engine()
        except TelemetryNotEnabledError:
            car.enable_telemetry()
            car.start_engine()
        if isinstance(car, HybridF1Car_v2):
            car.disable_boost()  # harvest energy until it's time to overtake

    def accelerate_car(self, car, fuel_amount_in_milliliters):
        try:
            car.push_accelerator(fuel_amount_in_milliliters)
        except NotEnoughFuelError:
            car.stop_engine()

    def overtake(self, car, fuel_amount_in_milliliters):
        if isinstance(car, HybridF1Car_v2):
            car.enable_boost()
        self.accelerate_car(car, fuel_amount_in_milliliters)
        if isinstance(car, HybridF1Car_v2):
            car.disable_boost()
