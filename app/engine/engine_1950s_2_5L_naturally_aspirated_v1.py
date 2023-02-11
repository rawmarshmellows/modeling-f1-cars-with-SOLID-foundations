class Engine1950s_2_5L_NaturallyAspirated_v1:
    def __init__(self):
        self.has_started = False

    def start(self):
        self.has_started = True
        print("Engine has started")

    def stop(self):
        self.has_started = False
        print("Engine has stopped")

    def inject_fuel(self, fuel):
        print(f"Inject {fuel.amount_in_milliliters}mL of fuel into engine")

    def inject_air(self):
        print("inject air into engine")

