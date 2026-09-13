from app.battery.electricity import Electricity


class EnergyRecoverySystem_v1:
    # The MGU-H recovers roughly 2.5MJ from the ~2.5L of fuel burned per lap,
    # so every mL of fuel burned gives back about 1kJ.
    KILOJOULES_RECOVERED_PER_MILLILITER = 1

    def recover_energy_from_mguh(self, fuel):
        return Electricity.create_from_amount_in_kilojoules(
            fuel.amount_in_milliliters * self.KILOJOULES_RECOVERED_PER_MILLILITER
        )
