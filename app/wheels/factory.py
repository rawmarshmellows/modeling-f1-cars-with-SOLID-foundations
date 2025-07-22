from .wheels_v1 import Wheels_v1

class WheelsFactory:
    @staticmethod
    def create_wheels_v1():
        return Wheels_v1()