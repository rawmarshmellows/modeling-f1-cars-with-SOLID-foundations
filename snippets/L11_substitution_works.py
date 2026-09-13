# ...continuing: build_hybrid_car, Driver_v2 and average_fuel_used_per_push come from the snippets above
from app.f1_cars.f1_car_with_telemetry_v1 import F1CarWithTelemetry_v1
from app.f1_cars.hybrid_f1_car_v2 import HybridF1Car_v2
from app.garage import build_telemetry_car

cars = [
    build_telemetry_car(F1CarWithTelemetry_v1),
    build_hybrid_car(HybridF1Car_v2),  # flat battery again
]
driver = Driver_v2()  # not a single line of the driver has changed
for car in cars:
    driver.start_car(car)
    for _ in range(10):
        driver.accelerate_car(car, fuel_amount_in_milliliters=8)

[len(car.get_telemetry_logs()) for car in cars]  # -> [10, 10]
[average_fuel_used_per_push(car.get_telemetry_logs()) for car in cars]  # -> [8.0, 8.0]
