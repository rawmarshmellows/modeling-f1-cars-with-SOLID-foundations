import subprocess
import sys

from snippets.catalog import ROOT

PIT_LANE = """\
from app.engine import EngineFactory
from app.f1_cars.f1_car_v5 import F1Car_v5

F1Car_v5(engine=EngineFactory.create_engine_1980s_1_5L_turbocharged_v3(), chassis=None, wheels=None, fuel_tank=None)
F1Car_v5(engine=EngineFactory.create_engine_1980s_1_5L_turbocharged_v1(), chassis=None, wheels=None, fuel_tank=None)
"""


def test_a_type_checker_rejects_an_engine_that_never_signed_the_contract(tmp_path):
    pit_lane = tmp_path / "pit_lane.py"
    pit_lane.write_text(PIT_LANE)
    result = subprocess.run(
        [sys.executable, "-m", "mypy", "--no-incremental", str(pit_lane)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    report = result.stdout
    assert "pit_lane.py:4" not in report, report  # the turbo that implements EngineInterface is accepted
    assert 'pit_lane.py:5: error: Argument "engine" to "F1Car_v5" has incompatible type "Engine1980s_1_5L_TurboCharged_v1"' in report, report
    # mypy also spots the factory that builds the engine which signed the contract without implementing start()
    assert 'Cannot instantiate abstract class "Engine1980s_1_5L_TurboCharged_v2"' in report, report
