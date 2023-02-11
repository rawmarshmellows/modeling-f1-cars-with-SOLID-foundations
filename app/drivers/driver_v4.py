from ..telemetry_system.exceptions import TelemetryNotEnabledError
from ..fuel_tank.exceptions import NotEnoughFuelError
from ..battery.exceptions import NotEnoughPowerError

class Driver_v4:
    def enable_car_telemetry(self, car):
        car.enable_telemetry()

    def start_car(self, car):
        try:
            car.start_engine()
        except TelemetryNotEnabledError:
            self.enable_car_telemetry(car)
            car.start_engine()

    def accelerate_car(self, car, fuel_amount):
        try:
            car.push_accelerator(fuel_amount)
        except NotEnoughPowerError:
            print("There isn't enough power, disable boost for now...")
            car.disable_boost()
            car.push_accelerator(fuel_amount)
        except NotEnoughFuelError:
            print("Engine is out of fuel turning engine off")
            car.stop_engine()

    def enable_boost(self, car):
        car.enable_boost()

    def disable_boost(self, car):
        car.disable_boost()