from app.f1_cars.f1_car_v1 import F1Car_v1


def test_engine_starts():
    f1_car = F1Car_v1()  # only the car knows which engine to build, so we build the whole car
    f1_car.start_engine()
    assert f1_car.engine.has_started


test_engine_starts()
