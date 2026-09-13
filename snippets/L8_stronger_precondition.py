# ...continuing from the previous snippet
driver.accelerate_car(hybrid, fuel_amount_in_milliliters=8)
# raises: InvalidFuelAmountError: The hybrid injector only takes fuel in multiples of 5mL, got 8mL
