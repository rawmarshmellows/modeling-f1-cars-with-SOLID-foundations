from app.chassis import ChassisFactory
from app.drivers.driver_v1 import Driver_v1
from app.engine import EngineFactory
from app.f1_cars.f1_car_v4 import F1Car_v4
from app.fuel_tank import FuelTankFactory
from app.wheels import WheelsFactory

turbo_car = F1Car_v4(
    engine=EngineFactory.create_engine_1980s_1_5L_turbocharged_v1(),
    chassis=ChassisFactory.create_chassis_monocoque_with_winged_sidepods_v1(),
    wheels=WheelsFactory.create_wheels_v1(),
    fuel_tank=FuelTankFactory.create_fuel_tank_v1(),
)
driver = Driver_v1()
driver.start_car(turbo_car)
# raises: AttributeError: 'Engine1980s_1_5L_TurboCharged_v1' object has no attribute 'start'
