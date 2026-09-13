from app.engine.engine_1950s_1_5L_supercharged_v1 import Engine1950s_1_5L_Supercharged_v1
from app.engine.engine_1950s_2_5L_naturally_aspirated_v1 import Engine1950s_2_5L_NaturallyAspirated_v1
from app.engine.engine_1960s_1_5L_naturally_aspirated_mid_rear_v1 import Engine1960s_1_5L_NaturallyAspirated_MidRear_v1
from app.engine.engine_1970s_1_5L_renault_rs01_v1 import Engine1970s_1_5L_Renault_RS01_v1
from app.engine.engine_1980s_1_5L_turbocharged_v1 import Engine1980s_1_5L_TurboCharged_v1
from app.engine.engine_1980s_1_5L_turbocharged_v2 import Engine1980s_1_5L_TurboCharged_v2
from app.engine.engine_1980s_1_5L_turbocharged_v3 import Engine1980s_1_5L_TurboCharged_v3
from app.engine.engine_2010s_1_6L_hybrid_turbocharged_v1 import Engine2010s_1_6L_HybridTurbocharged_v1


class EngineFactory:
    @staticmethod
    def create_engine_1950s_1_5L_supercharged_v1() -> Engine1950s_1_5L_Supercharged_v1:
        return Engine1950s_1_5L_Supercharged_v1()

    @staticmethod
    def create_engine_1950s_2_5L_naturally_aspirated_v1() -> Engine1950s_2_5L_NaturallyAspirated_v1:
        return Engine1950s_2_5L_NaturallyAspirated_v1()

    @staticmethod
    def create_engine_1960s_1_5L_naturally_aspirated_mid_rear_v1() -> Engine1960s_1_5L_NaturallyAspirated_MidRear_v1:
        return Engine1960s_1_5L_NaturallyAspirated_MidRear_v1()

    @staticmethod
    def create_engine_1970s_1_5L_renault_rs01_v1() -> Engine1970s_1_5L_Renault_RS01_v1:
        return Engine1970s_1_5L_Renault_RS01_v1()

    @staticmethod
    def create_engine_1980s_1_5L_turbocharged_v1() -> Engine1980s_1_5L_TurboCharged_v1:
        return Engine1980s_1_5L_TurboCharged_v1()

    @staticmethod
    def create_engine_1980s_1_5L_turbocharged_v2() -> Engine1980s_1_5L_TurboCharged_v2:
        return Engine1980s_1_5L_TurboCharged_v2()

    @staticmethod
    def create_engine_1980s_1_5L_turbocharged_v3() -> Engine1980s_1_5L_TurboCharged_v3:
        return Engine1980s_1_5L_TurboCharged_v3()

    @staticmethod
    def create_engine_2010s_1_6L_hybrid_turbocharged_v1() -> Engine2010s_1_6L_HybridTurbocharged_v1:
        return Engine2010s_1_6L_HybridTurbocharged_v1()
