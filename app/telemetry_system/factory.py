from .telemetry_system_v1 import TelemetrySystem_v1
from .telemetry_system_v2 import TelemetrySystem_v2

class TelemetrySystemFactory:
    @staticmethod
    def create_telemetry_system_v1():
        return TelemetrySystem_v1()

    def create_telemetry_system_v2():
        return TelemetrySystem_v2()