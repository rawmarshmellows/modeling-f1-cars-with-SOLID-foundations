from ..battery.electricity import Electricity

class EnergyRecoverySystem_v1:
    def __init__(self):
        pass

    def recovery_energy_from_mguh(self, fuel):
        # 1 mL of fuel = 277.7778 watts, this is calculated from the fact that
        # on average the MGU-H generates ~2.5MJ of power per lap, and the F1Car
        # uses ~2.5L of fuel per lap. 
        electricity = Electricity(fuel.amount_in_milliliters * 277.7778)
        print(f"Recovered {electricity.amount_in_watts}W from MGU-H")

        return electricity

    def recovery_energy_from_mguk(self):
        pass
