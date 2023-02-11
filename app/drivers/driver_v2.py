from ..fuel_tank.exceptions import NotEnoughFuelError

class Driver_v2:
    def start_car(self, car):
        car.start_engine()

    def accelerate_car(self, car, fuel_amount_in_milliliters):
        try:
            car.push_accelerator(fuel_amount_in_milliliters)
        except NotEnoughFuelError:
            print("Engine is out of fuel turning engine off")
            car.stop_engine()
    
    def enable_car_telemetry(self, car):
        car.enable_telemetry()
