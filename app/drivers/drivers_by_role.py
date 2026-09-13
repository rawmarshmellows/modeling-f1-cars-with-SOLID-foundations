from app.f1_cars.exceptions import StartRefusedError
from app.fuel_tank.exceptions import NotEnoughFuelError


def push_or_retire(car, fuel_amount_in_milliliters):
    try:
        car.push_accelerator(fuel_amount_in_milliliters)
    except NotEnoughFuelError:
        car.stop_engine()


class DriverForBasicCar:
    """For Startable + Accelerable cars."""

    def start_car(self, car):
        try:
            car.start_engine()
        except StartRefusedError as reason:
            print(f"The car refused to start: {reason}")

    def accelerate_car(self, car, fuel_amount_in_milliliters):
        push_or_retire(car, fuel_amount_in_milliliters)

    def overtake(self, car, fuel_amount_in_milliliters):
        push_or_retire(car, fuel_amount_in_milliliters)


class DriverForTelemetryCar:
    """For Startable + Accelerable + Telemetry cars: never starts an engine that isn't recorded."""

    def start_car(self, car):
        car.enable_telemetry()
        car.start_engine()

    def accelerate_car(self, car, fuel_amount_in_milliliters):
        push_or_retire(car, fuel_amount_in_milliliters)

    def overtake(self, car, fuel_amount_in_milliliters):
        push_or_retire(car, fuel_amount_in_milliliters)


class DriverForHybridCar:
    """For Startable + Accelerable + Telemetry + Boostable cars: harvests by default, deploys to overtake."""

    def start_car(self, car):
        car.enable_telemetry()
        car.start_engine()
        car.disable_boost()

    def accelerate_car(self, car, fuel_amount_in_milliliters):
        push_or_retire(car, fuel_amount_in_milliliters)

    def overtake(self, car, fuel_amount_in_milliliters):
        car.enable_boost()
        push_or_retire(car, fuel_amount_in_milliliters)
        car.disable_boost()
