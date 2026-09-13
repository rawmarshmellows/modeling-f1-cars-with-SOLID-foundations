# ...continuing from the previous snippet
hybrid.enable_telemetry()  # enable it by hand this time
driver.accelerate_car(hybrid, fuel_amount_in_milliliters=50)
first_snapshot = hybrid.get_telemetry_logs()[0]

for _ in range(9):
    driver.accelerate_car(hybrid, fuel_amount_in_milliliters=50)

first_snapshot in hybrid.get_telemetry_logs()  # -> False
len(hybrid.get_telemetry_logs())  # -> 5
