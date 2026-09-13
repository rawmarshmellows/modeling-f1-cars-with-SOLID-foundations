from app.fuel_tank.exceptions import NotEnoughFuelError


class FuelTank_v1:
    def __init__(self, current_fuel_in_tank):
        self.current_fuel_in_tank = current_fuel_in_tank

    def use_fuel(self, fuel):
        if fuel.amount_in_milliliters > self.current_fuel_in_tank.amount_in_milliliters:
            raise NotEnoughFuelError(
                f"There is not enough fuel! {fuel.amount_in_milliliters}mL requested "
                f"but only {self.current_fuel_in_tank.amount_in_milliliters}mL available"
            )
        self.current_fuel_in_tank -= fuel
