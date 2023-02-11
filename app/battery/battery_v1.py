from .electricity import  Electricity
from .exceptions import NotEnoughElectricityError

class Battery_v1:
    def __init__(self, current_electricity):
        self.current_electricity = current_electricity

    def use_electricity(self, electricity):
        amount_of_electricty_after_getting_electricity = (
            self.current_electricity - electricity
        ).amount_in_watts

        if amount_of_electricty_after_getting_electricity < 0:
            raise NotEnoughElectricityError(f"There is not enough electricity! {electricity.amount_in_watts}W requested but only {self.current_electricity.amount_in_watts}W available")

        self.current_electricity -= electricity
    
    def charge_electricity(self, electricity):
        self.current_electricity += electricity

