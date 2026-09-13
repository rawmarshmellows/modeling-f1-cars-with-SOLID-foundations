from app.drivers import DriverFactory
from app.f1_cars.f1_car_v7 import F1Car_v7
from app.f1_cars.f1_car_with_telemetry_v2 import F1CarWithTelemetry_v2
from app.f1_cars.hybrid_f1_car_v3 import HybridF1Car_v3
from app.garage import build_1950s_car, build_hybrid_car, build_telemetry_car

heritage_cars = [
    build_1950s_car(F1Car_v7),
    build_telemetry_car(F1CarWithTelemetry_v2),
    build_hybrid_car(HybridF1Car_v3, battery_charge_in_kilojoules=4_000),
]
for car in heritage_cars:
    driver = DriverFactory.create_driver_for(car)
    driver.start_car(car)
    driver.accelerate_car(car, fuel_amount_in_milliliters=50)
    driver.overtake(car, fuel_amount_in_milliliters=100)

[type(DriverFactory.create_driver_for(car)).__name__ for car in heritage_cars]
# -> ['DriverForBasicCar', 'DriverForTelemetryCar', 'DriverForHybridCar']
