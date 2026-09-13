from app.f1_cars.segregated_interfaces import (
    AccelerableInterface,
    BoostableInterface,
    StartableInterface,
    TelemetryInterface,
)


class F1Car_v7(StartableInterface, AccelerableInterface): ...


class F1CarWithTelemetry_v2(StartableInterface, AccelerableInterface, TelemetryInterface): ...


class HybridF1Car_v3(F1CarWithTelemetry_v2, BoostableInterface): ...
