class TelemetrySystem_v3:
    def __init__(self):
        self.is_enabled = False
        self.logs = []

    def save(self, log):
        if self.is_enabled is False:
            return
        self.logs.append(log)
    
    def enable(self):
        self.is_enabled = True
    
    def disable(self):
        self.is_enabled = False