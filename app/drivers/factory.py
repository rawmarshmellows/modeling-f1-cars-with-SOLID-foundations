from ..f1_cars.interface import HybridAccelerableInterface, NonHybridAccelerableInterface, TelemetryInterface
from .driver_for_hybrid_with_telemetry import DriverForHybridWithTelemetry
from .driver_for_non_hybrid_with_telemetry import DriverForNonHybridWithTelemetry
from .driver_for_non_hybrid_without_telemetry import DriverForNonHybridWithoutTelemetry

class DriverFactory:
    @staticmethod
    def create_driver_from_car(car):
        if issubclass(type(car), HybridAccelerableInterface):
            return DriverForHybridWithTelemetry()
        if issubclass(type(car), NonHybridAccelerableInterface) and not issubclass(type(car), TelemetryInterface):
            return DriverForNonHybridWithoutTelemetry()
        if issubclass(type(car), NonHybridAccelerableInterface) and issubclass(type(car), TelemetryInterface):
            return DriverForNonHybridWithTelemetry()