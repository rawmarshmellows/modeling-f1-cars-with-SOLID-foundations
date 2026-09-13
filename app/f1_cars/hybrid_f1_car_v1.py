from app.battery.electricity import Electricity
from app.f1_cars.f1_car_with_telemetry_v1 import F1CarWithTelemetry_v1
from app.f1_cars.hybrid_engine_interface import HybridEngineInterface
from app.fuel_tank.fuel import Fuel


class HybridF1Car_v1(F1CarWithTelemetry_v1):
    """The 2014 hybrid, ported in a hurry. Each change looks reasonable, and each one breaks the contract."""

    BOOST = Electricity.create_from_amount_in_kilojoules(120)
    MAX_TELEMETRY_LOGS = 5

    def __init__(self, engine: HybridEngineInterface, chassis, wheels, fuel_tank, telemetry_system, battery, energy_recovery_system):
        super().__init__(engine, chassis, wheels, fuel_tank, telemetry_system)
        self.battery = battery
        self.energy_recovery_system = energy_recovery_system
        self.boost_is_enabled = True

    def start_engine(self):
        # "The hybrid records so much data, the telemetry check is redundant"
        self.engine.start()

    def push_accelerator(self, fuel_amount_in_milliliters):
        # "Always deploy the boost, it's free speed"
        if self.boost_is_enabled:
            self.battery.use_electricity(self.BOOST)  # NotEnoughElectricityError on a flat battery
            self.engine.boost_with_electricity(self.BOOST)

        fuel = Fuel.create_from_amount_in_milliliters(fuel_amount_in_milliliters)
        self.engine.inject_air()
        self.fuel_tank.use_fuel(fuel)
        self.engine.inject_fuel(fuel)  # "The injector only takes 5mL pulses, callers will adapt"
        self.battery.charge_electricity(self.energy_recovery_system.recover_energy_from_mguh(fuel))
        self.telemetry_system.save(self.get_current_telemetry())

    def enable_boost(self):
        self.boost_is_enabled = True

    def disable_boost(self):
        self.boost_is_enabled = False

    def get_current_telemetry(self):
        # "Swap fuel for electricity to save radio bandwidth"
        return {"electricity_in_kilojoules": self.battery.current_electricity.amount_in_kilojoules}

    def get_telemetry_logs(self):
        # "Only the recent laps matter"
        return self.telemetry_system.logs[-self.MAX_TELEMETRY_LOGS:]
