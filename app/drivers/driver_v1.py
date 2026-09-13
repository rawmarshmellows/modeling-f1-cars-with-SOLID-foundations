from app.fuel_tank.exceptions import NotEnoughFuelError


class Driver_v1:
    def start_car(self, car):
        car.start_engine()

    def accelerate_car(self, car, fuel_amount_in_milliliters):
        try:
            car.push_accelerator(fuel_amount_in_milliliters)
        except NotEnoughFuelError:
            print("Out of fuel, turning the engine off")
            car.stop_engine()
