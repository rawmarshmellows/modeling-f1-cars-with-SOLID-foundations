from abc import ABC, abstractmethod

class EngineInterface(ABC):
    @abstractmethod
    def start():
        ...

    @abstractmethod
    def stop():
        ...

    @abstractmethod
    def inject_air():
        ...

    @abstractmethod
    def inject_fuel():
        ... 

class IsBoostableWithElectricityInterface(ABC):
    @abstractmethod
    def boost_with_electricity():
        ...
