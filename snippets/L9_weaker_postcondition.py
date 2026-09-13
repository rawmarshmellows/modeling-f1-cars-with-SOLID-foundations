# ...continuing from the previous snippet
def average_fuel_used_per_push(telemetry_logs):
    """Pit wall code, written against the promise in F1CarInterface.get_current_telemetry."""
    fuel = [log["fuel_in_milliliters"] for log in telemetry_logs]
    return (fuel[0] - fuel[-1]) / (len(fuel) - 1)


average_fuel_used_per_push(hybrid.get_telemetry_logs())
# raises: KeyError: 'fuel_in_milliliters'
