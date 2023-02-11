from .engine_1950s_2_5L_naturally_aspirated_v1 import Engine1950s_2_5L_NaturallyAspirated_v1
from .engine_1950s_2_5L_naturally_aspirated_v2 import Engine1950s_2_5L_NaturallyAspirated_v2
from .engine_1980s_1_5L_turbocharged_v1 import Engine1980s_1_5L_TurboCharged_v1
from .engine_1980s_1_5L_turbocharged_v2 import Engine1980s_1_5L_TurboCharged_v2
from .engine_1980s_1_5L_turbocharged_v3 import Engine1980s_1_5L_TurboCharged_v3
from.engine_2010s_1_6L_turbocharged_v1 import Engine_2010s_1_6L_Turbocharged_v1


class EngineFactory:
    @staticmethod
    def create_engine_1950s_2_5L_naturally_aspirated_v1():
        return Engine1950s_2_5L_NaturallyAspirated_v1()

    @staticmethod
    def create_engine_1950s_2_5L_naturally_aspirated_v2():
        return Engine1950s_2_5L_NaturallyAspirated_v2()
    
    @staticmethod
    def create_engine_1980s_1_5L_turbocharged_v1():
        return Engine1980s_1_5L_TurboCharged_v1()

    @staticmethod
    def create_engine_1980s_1_5L_turbocharged_v2():
        return Engine1980s_1_5L_TurboCharged_v2()

    @staticmethod
    def create_engine_1980s_1_5L_turbocharged_v3():
        return Engine1980s_1_5L_TurboCharged_v3()
    
    @staticmethod
    def create_engine_2010s_1_6L_turbocharged_v1():
        return Engine_2010s_1_6L_Turbocharged_v1()

