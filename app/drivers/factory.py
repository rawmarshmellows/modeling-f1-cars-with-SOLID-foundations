from app.drivers.drivers_by_role import DriverForBasicCar, DriverForHybridCar, DriverForTelemetryCar
from app.f1_cars.segregated_interfaces import BoostableInterface, TelemetryInterface


class DriverFactory:
    @staticmethod
    def create_driver_for(car):
        if isinstance(car, BoostableInterface) and isinstance(car, TelemetryInterface):
            return DriverForHybridCar()
        if isinstance(car, TelemetryInterface):
            return DriverForTelemetryCar()
        return DriverForBasicCar()
