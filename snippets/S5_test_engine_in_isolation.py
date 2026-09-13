from app.engine import EngineFactory


def test_engine_starts():
    engine = EngineFactory.create_engine_1950s_1_5L_supercharged_v1()  # built exactly as the car builds it
    engine.start()
    assert engine.has_started


test_engine_starts()
