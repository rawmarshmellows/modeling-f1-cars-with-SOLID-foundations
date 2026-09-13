# ...continuing from the previous snippet
hybrid = build_hybrid_car(HybridF1Car_v1, battery_charge_in_kilojoules=4_000)
driver.start_car(hybrid)  # no TelemetryNotEnabledError, so the driver never enables telemetry
driver.accelerate_car(hybrid, fuel_amount_in_milliliters=50)

hybrid.engine.has_started, hybrid.telemetry_system.is_enabled  # -> (True, False)
hybrid.get_telemetry_logs()  # -> []
