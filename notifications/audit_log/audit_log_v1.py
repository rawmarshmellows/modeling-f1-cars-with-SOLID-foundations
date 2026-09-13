class AuditLog_v1:
    def __init__(self):
        self.is_enabled = False
        self.entries = []

    def record(self, entry):
        if self.is_enabled:
            self.entries.append(entry)

    def enable(self):
        self.is_enabled = True

    def disable(self):
        self.is_enabled = False
