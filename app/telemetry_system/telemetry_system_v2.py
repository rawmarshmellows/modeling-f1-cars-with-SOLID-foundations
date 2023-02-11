class TelemetrySystem_v2:
    def __init__(self):
        self.is_enabled = False
        self.logs = []
        self.log_count = 0
        self.max_number_of_logs = 5

    def save(self, log):
        if self.is_enabled is False:
            return
        
        if len(self.logs) < self.max_number_of_logs:
            self.logs.append(log)
        else:
            self.logs = self.logs[1:] + [log]
    
    def enable(self):
        self.is_enabled = True
    
    def disable(self):
        self.is_enabled = False