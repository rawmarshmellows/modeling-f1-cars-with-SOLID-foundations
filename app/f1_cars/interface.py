from abc import ABC, abstractmethod


class F1CarInterface(ABC):
    """Every car the team has built since telemetry arrived in the late 1980s.

    The signatures are half of the contract. The docstrings are the other half,
    and the drivers and the pit wall rely on both.

    Invariant: the engine only ever runs while telemetry is recording.
    """

    @abstractmethod
    def start_engine(self):
        """Raises TelemetryNotEnabledError instead of starting an engine that isn't being recorded."""

    @abstractmethod
    def stop_engine(self): ...

    @abstractmethod
    def push_accelerator(self, fuel_amount_in_milliliters):
        """Draws exactly `fuel_amount_in_milliliters` from the tank, for any positive amount.

        Raises NotEnoughFuelError when the tank runs dry, and nothing else.
        """

    @abstractmethod
    def enable_telemetry(self): ...

    @abstractmethod
    def disable_telemetry(self):
        """Stops the engine first, so it never runs unrecorded."""

    @abstractmethod
    def get_current_telemetry(self):
        """A snapshot of the car that always includes "fuel_in_milliliters"."""

    @abstractmethod
    def get_telemetry_logs(self):
        """Every snapshot taken since telemetry was enabled, oldest first.

        The log only grows: a snapshot, once recorded, never disappears.
        """
