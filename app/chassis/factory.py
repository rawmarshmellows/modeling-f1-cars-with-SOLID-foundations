from .chassis_v1 import Chassis_v1

class ChassisFactory:
    @staticmethod
    def create_chassis_v1():
        return Chassis_v1()