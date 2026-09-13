from app.f1_cars.engine_interface import EngineInterface


class Engine1950s_1_5L_Supercharged_v1(EngineInterface):
    def __init__(self):
        self.has_started = False

    def start(self):
        self.has_started = True
        print("Engine has started")

    def stop(self):
        self.has_started = False
        print("Engine has stopped")

    def inject_air(self):
        print("Inject air into engine through supercharger")

    def inject_fuel(self, fuel):
        print(f"Inject {fuel.amount_in_milliliters}mL of fuel into engine")
