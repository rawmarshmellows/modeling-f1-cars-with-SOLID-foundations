from app.engine.exceptions import InvalidFuelAmountError
from app.f1_cars.hybrid_engine_interface import HybridEngineInterface


class Engine2010s_1_6L_HybridTurbocharged_v1(HybridEngineInterface):
    def __init__(self):
        self.has_started = False

    def start(self):
        self.has_started = True
        print("Hybrid power unit has started")

    def stop(self):
        self.has_started = False
        print("Hybrid power unit has stopped")

    def inject_air(self):
        print("Inject air into engine through turbocharger")

    def inject_fuel(self, fuel):
        if fuel.amount_in_milliliters % 5 != 0:
            raise InvalidFuelAmountError(
                f"The hybrid injector only takes fuel in multiples of 5mL, got {fuel.amount_in_milliliters}mL"
            )
        print(f"Inject {fuel.amount_in_milliliters}mL of fuel into engine")

    def boost_with_electricity(self, electricity):
        print(f"Boost engine with {electricity.amount_in_kilojoules}kJ from the battery")
