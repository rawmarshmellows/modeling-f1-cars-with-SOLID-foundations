from app.battery.exceptions import NotEnoughElectricityError


class Battery_v1:
    def __init__(self, current_electricity):
        self.current_electricity = current_electricity

    def can_supply(self, electricity):
        return electricity.amount_in_kilojoules <= self.current_electricity.amount_in_kilojoules

    def use_electricity(self, electricity):
        if not self.can_supply(electricity):
            raise NotEnoughElectricityError(
                f"There is not enough electricity! {electricity.amount_in_kilojoules}kJ requested "
                f"but only {self.current_electricity.amount_in_kilojoules}kJ available"
            )
        self.current_electricity -= electricity

    def charge_electricity(self, electricity):
        self.current_electricity += electricity
