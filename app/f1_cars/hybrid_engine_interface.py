from abc import abstractmethod

from app.f1_cars.engine_interface import EngineInterface


class HybridEngineInterface(EngineInterface):
    @abstractmethod
    def boost_with_electricity(self, electricity): ...
