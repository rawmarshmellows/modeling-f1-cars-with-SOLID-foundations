from ..fuel_tank.exceptions import NotEnoughFuelError

class DriverForNonHybridWithoutTelemetry:
    def start_car(self, car):
        car.start_engine(car)

    def accelerate_car(self, car, fuel_amount):
        try:
            car.push_accelerator(fuel_amount)
        except NotEnoughFuelError:
            car.stop_engine()

