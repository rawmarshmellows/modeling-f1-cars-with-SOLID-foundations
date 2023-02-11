from .energy_recovery_system_v1 import EnergyRecoverySystem_v1

class EnergyRecoverySystemFactory:
    @staticmethod
    def create_energy_recovery_system_v1():
        return EnergyRecoverySystem_v1()    
