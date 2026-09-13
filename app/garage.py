"""The composition root: the one place that knows which parts go into which car.

Later examples use these builders so the snippets can focus on behaviour, not wiring.
"""

from app.battery import BatteryFactory
from app.chassis import ChassisFactory
from app.energy_recovery_system import EnergyRecoverySystemFactory
from app.engine import EngineFactory
from app.fuel_tank import FuelTankFactory
from app.telemetry_system import TelemetrySystemFactory
from app.wheels import WheelsFactory


def build_1950s_car(car_class):
    return car_class(
        engine=EngineFactory.create_engine_1950s_2_5L_naturally_aspirated_v1(),
        chassis=ChassisFactory.create_chassis_spaceframe_v1(),
        wheels=WheelsFactory.create_wheels_v1(),
        fuel_tank=FuelTankFactory.create_fuel_tank_v1(),
    )


def build_telemetry_car(car_class):
    return car_class(
        engine=EngineFactory.create_engine_1980s_1_5L_turbocharged_v3(),
        chassis=ChassisFactory.create_chassis_monocoque_with_winged_sidepods_v1(),
        wheels=WheelsFactory.create_wheels_v1(),
        fuel_tank=FuelTankFactory.create_fuel_tank_v1(),
        telemetry_system=TelemetrySystemFactory.create_telemetry_system_v1(),
    )


def build_hybrid_car(car_class, battery_charge_in_kilojoules=0):
    return car_class(
        engine=EngineFactory.create_engine_2010s_1_6L_hybrid_turbocharged_v1(),
        chassis=ChassisFactory.create_chassis_monocoque_v1(),
        wheels=WheelsFactory.create_wheels_v1(),
        fuel_tank=FuelTankFactory.create_fuel_tank_v1(),
        telemetry_system=TelemetrySystemFactory.create_telemetry_system_v1(),
        battery=BatteryFactory.create_battery_v1(battery_charge_in_kilojoules),
        energy_recovery_system=EnergyRecoverySystemFactory.create_energy_recovery_system_v1(),
    )
