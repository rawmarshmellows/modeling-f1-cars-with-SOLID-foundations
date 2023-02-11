from .exceptions import InvalidFuelAmountError
from .interface import EngineInterface, IsBoostableWithElectricityInterface

class Engine_2010s_1_6L_Hybrid_Turbocharged_v1(EngineInterface, IsBoostableWithElectricityInterface):
    def __init__(self):
        self.has_started = False

    def start(self):
        self.start_with_turbocharger()

    def start_with_turbocharger(self):
        self.has_started = True
        print("Engine has started with turbocharger")

    def stop(self):
        self.has_started = False
        print("Engine has stopped")

    def inject_fuel(self, fuel):
        if fuel.amount_in_milliliters % 5 != 0:
            raise InvalidFuelAmountError("Fuel amount in milliliters injected is not in multiples of 5")
        print(f"Inject {fuel.amount_in_milliliters}mL of fuel into engine with better efficiency")            

    def inject_air(self):
        print("Inject air into engine with better efficiency")
    
    def boost_with_electricity(self, electricity):
        print(f"Boost engine with {electricity.amount_in_watts}W of electricity")

