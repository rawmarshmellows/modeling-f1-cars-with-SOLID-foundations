from ..fuel_tank.exceptions import NotEnoughFuelError
from ..battery.exceptions import NotEnoughElectricityError

class DriverForHybridWithTelemetry:
    def start_car(self, car):
        car.enable_telemetry()
        car.start_engine()

    def accelerate_car(self, car, fuel_amount_in_milliliters):
        amount_to_round_up = 5 - fuel_amount_in_milliliters % 5
        fuel_amount_in_milliliters_rounded_up_to_nearest_multiple_of_five = (
            fuel_amount_in_milliliters + amount_to_round_up
        )
        try:
            car.push_accelerator(fuel_amount_in_milliliters_rounded_up_to_nearest_multiple_of_five)
        except NotEnoughElectricityError:
            car.disable_boost()
            self.accelerate_car(car, fuel_amount_in_milliliters_rounded_up_to_nearest_multiple_of_five)
        except NotEnoughFuelError:
            car.stop_engine()

    def enable_car_telemetry(self, car):
        car.enable_telemetry()

    def enable_boost(self, car):    
        car.enable_boost()