from ..telemetry_system import TelemetryNotEnabledError
from ..telemetry_system.telemetry_system_v2 import TelemetrySystem_v2
from .interface import F1CarInterface
from ..fuel_tank.fuel import Fuel
from ..battery.electricity import Electricity
from ..engine.interface import IsBoostableWithElectricityInterface

class HybridF1CarWithTelemetry_v2(F1CarInterface):
    def __init__(self, engine, chassis, wheels, fuel_tank, telemetry_system, battery, energy_recovery_system):

        if not issubclass(type(engine), IsBoostableWithElectricityInterface):
            raise TypeError("Engine must implement the IsBoostableWithElectricityInterface")

        self.engine = engine
        self.chassis = chassis
        self.wheels = wheels
        self.fuel_tank = fuel_tank
        self.telemetry_system = telemetry_system
        self.battery = battery
        self.energy_recovery_system = energy_recovery_system
        self.boost_is_enabled = False

    def push_accelerator(self, fuel_amount_in_milliliters):
        if self.boost_is_enabled:
            electricity = Electricity.create_from_amount_in_watts(120000)
            self.battery.use_electricity(electricity)
            self.engine.boost_with_electricity(electricity)

        fuel = Fuel.create_from_amount_in_milliliters(fuel_amount_in_milliliters)
        self.engine.inject_air()
        self.fuel_tank.use_fuel(fuel)
        self.engine.inject_fuel(fuel)
        electricity = self.energy_recovery_system.recovery_energy_from_mguh(fuel)
        self.battery.charge_electricity(electricity)
        self.save_current_telemetry()

    def start_engine(self):
        if not self.telemetry_system.is_enabled:
            raise TelemetryNotEnabledError(
                "The Engine has started but the telemetry hasn't been enabled!"
            )
        self.engine.start()

    def stop_engine(self):
        self.engine.stop()

    def enable_boost(self):
        self.boost_is_enabled = True

    def disable_boost(self):
        self.boost_is_enabled = False

    def enable_telemetry(self):
        self.telemetry_system.enable()

    def disable_telemetry(self):
        self.telemetry_system.disable()

    def get_current_telemetry(self):
        return {
            "electricity": self.battery.current_electricity.amount_in_watts,
        }

    def get_telemetry_logs(self):
        return self.telemetry_system.logs

    def save_current_telemetry(self):
        current_telemetry = self.get_current_telemetry()
        self.telemetry_system.save(current_telemetry)