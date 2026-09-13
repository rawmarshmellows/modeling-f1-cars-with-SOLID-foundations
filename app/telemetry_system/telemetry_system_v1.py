class TelemetrySystem_v1:
    def __init__(self):
        self.is_enabled = False
        self.logs = []

    def save(self, log):
        if self.is_enabled:
            self.logs.append(log)

    def enable(self):
        self.is_enabled = True

    def disable(self):
        self.is_enabled = False
