# ...continuing from the previous snippet

# 1962: Lotus 25 style, mid-rear engine in a monocoque chassis
f1_car_1962 = F1Car_v4(
    engine=EngineFactory.create_engine_1960s_1_5L_naturally_aspirated_mid_rear_v1(),
    chassis=ChassisFactory.create_chassis_monocoque_v1(),
    wheels=WheelsFactory.create_wheels_v1(),
    fuel_tank=FuelTankFactory.create_fuel_tank_v1(),
)

# 1977: Renault RS01 turbo engine with Lotus 78 ground-effect sidepods
f1_car_1977 = F1Car_v4(
    engine=EngineFactory.create_engine_1970s_1_5L_renault_rs01_v1(),
    chassis=ChassisFactory.create_chassis_monocoque_with_winged_sidepods_v1(),
    wheels=WheelsFactory.create_wheels_v1(),
    fuel_tank=FuelTankFactory.create_fuel_tank_v1(),
)

# Three eras, one class, zero edits to F1Car_v4
[type(car.engine).__name__ for car in (f1_car_1954, f1_car_1962, f1_car_1977)]
# -> ['Engine1950s_2_5L_NaturallyAspirated_v1', 'Engine1960s_1_5L_NaturallyAspirated_MidRear_v1', 'Engine1970s_1_5L_Renault_RS01_v1']
