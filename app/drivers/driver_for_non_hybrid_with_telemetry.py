from ..fuel_tank.exceptions import NotEnoughFuelError
from ..battery.exceptions import NotEnoughElectricityError

class DriverForNonHybridWithTelemetry:
    def start_car(self, car):
        car.enable_telemetry()
        car.start_engine()

    def accelerate_car(self, car, fuel_amount_in_milliliters):
        try:
            car.push_accelerator(fuel_amount_in_milliliters)
        except NotEnoughElectricityError:
            car.disable_boost()
            self.accelerate_car(car, fuel_amount_in_milliliters)
        except NotEnoughFuelError:
            car.stop_engine()

    def enable_car_telemetry(self, car):
        car.enable_telemetry()

    def enable_boost(self, car):    
        car.enable_boost()