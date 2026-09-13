from app.chassis import ChassisFactory
from app.engine import EngineFactory
from app.f1_cars.f1_car_v4 import F1Car_v4
from app.fuel_tank import FuelTankFactory
from app.wheels import WheelsFactory

f1_car_1954 = F1Car_v4(
    engine=EngineFactory.create_engine_1950s_2_5L_naturally_aspirated_v1(),
    chassis=ChassisFactory.create_chassis_spaceframe_v1(),
    wheels=WheelsFactory.create_wheels_v1(),
    fuel_tank=FuelTankFactory.create_fuel_tank_v1(),
)
f1_car_1954.start_engine()
f1_car_1954.engine.has_started  # -> True
