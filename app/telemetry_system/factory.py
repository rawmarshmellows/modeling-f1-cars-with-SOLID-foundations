from app.telemetry_system.telemetry_system_v1 import TelemetrySystem_v1


class TelemetrySystemFactory:
    @staticmethod
    def create_telemetry_system_v1():
        return TelemetrySystem_v1()
