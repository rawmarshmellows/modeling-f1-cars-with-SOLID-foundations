from abc import ABC, abstractmethod


class StartableInterface(ABC):
    @abstractmethod
    def start_engine(self):
        """Raises StartRefusedError (or a subclass of it) if the car isn't ready to start."""

    @abstractmethod
    def stop_engine(self): ...


class AccelerableInterface(ABC):
    @abstractmethod
    def push_accelerator(self, fuel_amount_in_milliliters):
        """Draws exactly `fuel_amount_in_milliliters` from the tank, for any positive amount.

        Raises NotEnoughFuelError when the tank runs dry, and nothing else.
        """


class TelemetryInterface(ABC):
    """Invariant: the engine only ever runs while telemetry is recording.

    To keep it, start_engine refuses with TelemetryNotEnabledError, a StartRefusedError.
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


class BoostableInterface(ABC):
    @abstractmethod
    def enable_boost(self): ...

    @abstractmethod
    def disable_boost(self): ...
