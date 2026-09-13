from abc import ABC, abstractmethod


class EngineInterface(ABC):
    """The car team's spec: what every engine must do to go in one of our cars."""

    @abstractmethod
    def start(self): ...

    @abstractmethod
    def stop(self): ...

    @abstractmethod
    def inject_air(self): ...

    @abstractmethod
    def inject_fuel(self, fuel): ...
