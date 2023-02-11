from .chassis_spaceframe_v1 import Chassis_Spaceframe_v1
from .chassis_monocoque_v1 import Chassis_Monocoque_v1
from .chassis_monocoque_with_winged_sidepods_v1 import Chassis_Monocoque_With_WingedSidepods_v1 

class ChassisFactory:
    @staticmethod
    def create_chassis_spaceframe_v1():
        return Chassis_Spaceframe_v1()
    
    @staticmethod
    def create_chassis_monocoque_v1():
        return Chassis_Monocoque_v1()

    @staticmethod
    def create_chassis_monocoque_with_winged_sidepods_v1():
        return Chassis_Monocoque_With_WingedSidepods_v1()