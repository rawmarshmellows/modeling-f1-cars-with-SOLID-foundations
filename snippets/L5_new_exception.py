from app.drivers.driver_v2 import Driver_v2
from app.f1_cars.hybrid_f1_car_v1 import HybridF1Car_v1
from app.garage import build_hybrid_car

hybrid = build_hybrid_car(HybridF1Car_v1)  # the battery leaves the garage flat
driver = Driver_v2()
driver.start_car(hybrid)
driver.accelerate_car(hybrid, fuel_amount_in_milliliters=50)
# raises: NotEnoughElectricityError: There is not enough electricity! 120kJ requested but only 0kJ available
