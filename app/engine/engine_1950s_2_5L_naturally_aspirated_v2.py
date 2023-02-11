class Engine1950s_2_5L_NaturallyAspirated_v2:
    def __init__(self):
        self.has_started = False

    def start(self):
        self.has_started = True
        print("engine has started")

    def stop(self):
        self.has_started = False
        print("engine has stopped")

    def inject_fuel(self, fuel):
        print(f"inject fuel {fuel} into engine with better efficiency")

    def inject_air(self):
        print("logic to inject air into engine")

