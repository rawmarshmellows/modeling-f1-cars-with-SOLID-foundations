# ...continuing from the previous snippet (error message as worded by Python 3.12+)
# Engine1980s_1_5L_TurboCharged_v2 subclasses EngineInterface, but still has no start()
EngineFactory.create_engine_1980s_1_5L_turbocharged_v2()
# raises: TypeError: Can't instantiate abstract class Engine1980s_1_5L_TurboCharged_v2 without an implementation for abstract method 'start'
