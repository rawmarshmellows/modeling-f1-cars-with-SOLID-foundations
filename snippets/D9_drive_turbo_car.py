# ...continuing from the previous snippet
from app.f1_cars.f1_car_v5 import F1Car_v5

turbo_car = F1Car_v5(
    engine=EngineFactory.create_engine_1980s_1_5L_turbocharged_v3(),
    chassis=ChassisFactory.create_chassis_monocoque_with_winged_sidepods_v1(),
    wheels=WheelsFactory.create_wheels_v1(),
    fuel_tank=FuelTankFactory.create_fuel_tank_v1(),
)
driver.start_car(turbo_car)  # the same Driver_v1, and a car that never learned about turbos
turbo_car.engine.has_started  # -> True
