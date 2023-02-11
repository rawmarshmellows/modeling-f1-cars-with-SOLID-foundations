from abc import ABC, abstractmethod

class F1CarInterface(ABC):
    @abstractmethod
    def push_accelerator(self):
        ...

    @abstractmethod
    def start_engine(self):
        ...

    @abstractmethod
    def stop_engine(self):
        ...

    @abstractmethod
    def get_current_telemetry(self):
        ...
    
    @abstractmethod
    def get_telemetry_logs(self):
        ...

    @abstractmethod
    def save_current_telemetry(self):
        ...

    @abstractmethod
    def enable_telemetry(self):
        ...

    @abstractmethod
    def disable_telemetry(self):
        ...

class NonHybridAccelerableInterface(ABC):
    @abstractmethod
    def push_accelerator(self):
        ...


class HybridAccelerableInterface(ABC):
    @abstractmethod
    def push_accelerator(self):
        ...

    @abstractmethod
    def enable_boost(self):
        ...

    @abstractmethod
    def disable_boost(self):
        ...


class TelemetryInterface(ABC):
    @abstractmethod
    def get_telemetry_logs(self):
        ...

    @abstractmethod
    def get_current_telemetry(self):
        ...

    @abstractmethod
    def save_current_telemetry(self):
        ...

    @abstractmethod
    def enable_telemetry(self):
        ...

    @abstractmethod
    def disable_telemetry(self):
        ...


class StartableInterface(ABC):
    @abstractmethod
    def start_engine(self):
        ...

    @abstractmethod
    def stop_engine(self):
        ...