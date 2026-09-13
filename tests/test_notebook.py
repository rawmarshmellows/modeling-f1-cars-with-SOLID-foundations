import subprocess
import sys

from snippets.catalog import ROOT


def test_notebook_runs_top_to_bottom_as_a_script():
    result = subprocess.run(
        [sys.executable, "notebook.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, result.stderr[-3000:]


def test_notebook_passes_marimo_check():
    result = subprocess.run(
        [sys.executable, "-m", "marimo", "check", "--strict", "notebook.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, result.stdout + result.stderr
