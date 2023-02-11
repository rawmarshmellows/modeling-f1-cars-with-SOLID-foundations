from ..telemetry_system import TelemetryNotEnabledError
from ..telemetry_system.telemetry_system_v2 import TelemetrySystem_v2
from .interface import F1CarInterface

class HybridF1CarWithTelemetry_v3(F1CarInterface):
    def __init__(self, engine, chassis, wheels, fuel_tank, telemetry_system, battery):
        if type(telemetry_system) != TelemetrySystem_v2:
            raise TypeError("Telemetry system must be of type TelemetrySystem_v2")
        self.engine = engine
        self.chassis = chassis
        self.wheels = wheels
        self.fuel_tank = fuel_tank
        self.telemetry_system = telemetry_system
        self.battery = battery
        self.boost_is_enabled = False

    # get better units between conversion rate of fuel usage and watts
    def push_accelerator(self, fuel_amount):
        self.save_current_telemetry()
        if self.boost_is_enabled:
            electricity = self.battery.use_electricity(5)
            print(f"boost car with electricity of {electricity.amount} watts")
        self.engine.inject_air()
        fuel = self.fuel_tank.use_fuel(fuel_amount)
        self.engine.inject_fuel(fuel)
        self.battery.charge_electricity(fuel_amount)

    def start_engine(self):
        if not self.telemetry_system.is_enabled:
            raise TelemetryNotEnabledError(
                "The engine has started but the telemetry hasn't been enabled!"
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
            "electricity": self.battery.current_electricity.amount,
            "fuel": self.fuel_tank.current_fuel_in_tank.amount
        }
        
    def get_telemetry_logs(self):
        return self.telemetry_system.logs

    def save_current_telemetry(self):
        current_telemetry = self.get_current_telemetry()
        self.telemetry_system.save(current_telemetry)