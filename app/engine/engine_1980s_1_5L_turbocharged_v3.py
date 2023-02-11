from .interface import EngineInterface

class Engine1980s_1_5L_TurboCharged_v3(EngineInterface):
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
        print(f"Inject {fuel.amount_in_milliliters}mL of fuel into engine with better efficiency")

    def inject_air(self):
        print("Inject air into engine with better efficiency")

