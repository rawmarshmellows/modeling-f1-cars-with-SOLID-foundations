from ..telemetry_system.exceptions import TelemetryNotEnabledError
from ..fuel_tank.exceptions import NotEnoughFuelError
from ..battery.exceptions import NotEnoughElectricityError
from ..engine.exceptions import InvalidFuelAmountError

class Driver_v5:
    def enable_car_telemetry(self, car):
        car.enable_telemetry()

    def start_car(self, car):
        try:
            car.start_engine()
        except TelemetryNotEnabledError:
            print("Car telemetry is not enabled. Enabling car telemetry...")
            self.enable_car_telemetry(car)
            car.start_engine()

    def accelerate_car(self, car, fuel_amount_in_milliliters):
        try:
            car.push_accelerator(fuel_amount_in_milliliters)
        except NotEnoughElectricityError:
            print("There isn't enough electricity, disable boost for now...")
            car.disable_boost()
            car.push_accelerator(fuel_amount_in_milliliters)
        except NotEnoughFuelError:
            print("Engine is out of fuel turning engine off")
            car.stop_engine()
        except InvalidFuelAmountError:
            amount_to_round_up = 5 - fuel_amount_in_milliliters % 5
            fuel_amount_in_milliliters_rounded_up_to_nearest_multiple_of_five = (
                fuel_amount_in_milliliters + amount_to_round_up
            )
            print(f"Fuel amount used was {fuel_amount_in_milliliters} but amount is invalid so rounding up to {fuel_amount_in_milliliters_rounded_up_to_nearest_multiple_of_five}")
            self.accelerate_car(car, fuel_amount_in_milliliters_rounded_up_to_nearest_multiple_of_five)

    def enable_boost(self, car):
        car.enable_boost()

    def disable_boost(self, car):
        car.disable_boost()