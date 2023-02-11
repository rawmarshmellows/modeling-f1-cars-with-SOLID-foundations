class Engine1980s_1_5L_TurboCharged_v1:
    def __init__(self):
        self.has_started = False

    def start_with_turbocharger(self):
        self.has_started = True
        print("engine has started with turbocharger")

    def stop(self):
        self.has_started = False
        print("engine has stopped")

    def inject_fuel(self, fuel):
        print(f"inject fuel into engine with better efficiency")

    def inject_air(self):
        print("inject air into engine with better efficiency")

