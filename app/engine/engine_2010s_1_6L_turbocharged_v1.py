from .exceptions import InvalidFuelAmountError
from .interface import EngineInterface

class Engine_2010s_1_6L_Turbocharged_v1(EngineInterface):
    def __init__(self):
        self.has_started = False

    def start(self):
        self.start_with_turbocharger()

    def start_with_turbocharger(self):
        self.has_started = True
        print("engine has started with turbocharger")

    def stop(self):
        self.has_started = False
        print("engine has stopped")

    def inject_fuel(self, fuel):
        if fuel.amount % 5 != 0:
            raise InvalidFuelAmountError("Fuel amount inject is not in multiples of 5")
        print(f"inject fuel into engine with better efficiency")

    def inject_air(self):
        print("inject air into engine with better efficiency")

