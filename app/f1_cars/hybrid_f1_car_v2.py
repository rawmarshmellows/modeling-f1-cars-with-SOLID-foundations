from app.battery.electricity import Electricity
from app.f1_cars.f1_car_with_telemetry_v1 import F1CarWithTelemetry_v1
from app.f1_cars.hybrid_engine_interface import HybridEngineInterface
from app.fuel_tank.fuel import Fuel


class HybridF1Car_v2(F1CarWithTelemetry_v1):
    """The 2014 hybrid, built to stand in for any F1CarInterface car.

    start_engine and get_telemetry_logs are inherited untouched, so the
    telemetry invariant and the log history both survive.
    """

    BOOST = Electricity.create_from_amount_in_kilojoules(120)
    INJECTOR_PULSE_IN_MILLILITERS = 5

    def __init__(self, engine: HybridEngineInterface, chassis, wheels, fuel_tank, telemetry_system, battery, energy_recovery_system):
        super().__init__(engine, chassis, wheels, fuel_tank, telemetry_system)
        self.battery = battery
        self.energy_recovery_system = energy_recovery_system
        self.boost_is_enabled = True
        self._fuel_waiting_for_injector_in_milliliters = 0

    def push_accelerator(self, fuel_amount_in_milliliters):
        fuel = Fuel.create_from_amount_in_milliliters(fuel_amount_in_milliliters)
        self.fuel_tank.use_fuel(fuel)  # draws exactly what was asked, before anything else happens

        # No new exceptions: a flat battery means no boost, not a crash
        if self.boost_is_enabled and self.battery.can_supply(self.BOOST):
            self.battery.use_electricity(self.BOOST)
            self.engine.boost_with_electricity(self.BOOST)

        # No stronger precondition: any amount is accepted, the 5mL injector is the car's problem
        self.engine.inject_air()
        burned_fuel = self._take_whole_injector_pulses(fuel)
        if burned_fuel.amount_in_milliliters:
            self.engine.inject_fuel(burned_fuel)
        self.battery.charge_electricity(self.energy_recovery_system.recover_energy_from_mguh(burned_fuel))
        self.telemetry_system.save(self.get_current_telemetry())

    def _take_whole_injector_pulses(self, fuel):
        waiting = self._fuel_waiting_for_injector_in_milliliters + fuel.amount_in_milliliters
        leftover = waiting % self.INJECTOR_PULSE_IN_MILLILITERS
        self._fuel_waiting_for_injector_in_milliliters = leftover
        return Fuel.create_from_amount_in_milliliters(waiting - leftover)

    def enable_boost(self):
        self.boost_is_enabled = True

    def disable_boost(self):
        self.boost_is_enabled = False

    def get_current_telemetry(self):
        # No weaker postcondition: everything the parent reported, plus the battery
        return {
            **super().get_current_telemetry(),
            "electricity_in_kilojoules": self.battery.current_electricity.amount_in_kilojoules,
        }
