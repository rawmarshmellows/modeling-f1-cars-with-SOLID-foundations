# Driving Change: SOLID in Python, Told Through an F1 Car: Outline (v2)

> **Built (2026-09-13).** `snippets/manifest.toml` is now the source of truth for the gist list. The outline below is the approved plan; here's what changed during the build:
> - 36 gists, not 31. D got 9 (the engine and car changes are shown as `.diff` gists), L got 11 (the interface and the base car are separate gists, and the proof that substitution works has its own), and I got 7 (the heritage demo-day run has its own).
> - Changes after the technical review:
>   - Dependency Inversion: `EngineInterface` now lives in the car team's package, a new `F1Car_v5` declares `engine: EngineInterface`, and every engine except the pre-contract turbo implements it. A mypy test backs the type-checker claim.
>   - Liskov: the invariant is a real one (`disable_telemetry` stops the engine), and the history example shows a recorded snapshot disappearing.
>   - Interface Segregation: `StartableInterface` documents `StartRefusedError`. The 1950s cars are now `F1Car_v6` (the stubs) and `F1Car_v7` (the split interfaces).
> - Liskov: every violation lives in `HybridF1Car_v1`, which subclasses `F1CarWithTelemetry_v1`. `HybridF1Car_v2` fixes all of them inside the car, and `Driver_v2` never changes. The history violation lives in the car (`get_telemetry_logs` returns the last 5 logs), not in a separate telemetry system.
> - Interface Segregation: the interfaces are `Startable`, `Accelerable`, `Telemetry` and `Boostable`, instead of splitting hybrid and non-hybrid acceleration. The role-based drivers deliberately don't inherit from each other, because a hybrid driver's stronger precondition would itself break Liskov.
> - Units: fuel is stored in mL and electricity in kJ, both as integers, so the telemetry numbers in the snippets come out exact.


**Locked decisions**
- Order: S → O → D → L → I (D introduces the interfaces that L and I build on).
- One article. One F1 story per letter, and the rest is code.
- The marimo notebook follows the article exactly. Every code example in the notebook is one gist.
- Liskov: every violation comes from a single swap, the 2014 hybrid replacing the 1980s telemetry car.

---

## 0. Intro (~150 words, 0 gists)
- Hook: F1 rewrites its rulebook almost every season, and your product requirements change just as often.
- What the reader gets: five principles, one real refactor for each, and a repo they can run.
- Run it: `git clone … && cd … && uv run marimo edit notebook.py`

## S: Single Responsibility (5 gists)
**F1 story:** 1951. Alfa Romeo swaps 159 engines between races. (1 image)

| #  | Gist                            | Shows                                                   |
|----|---------------------------------|---------------------------------------------------------|
| S1 | `f1_car_v1.py`                  | The car builds its own engine, chassis, wheels and tank |
| S2 | `test_engine_needs_whole_car.py`| The only way to test the engine is to build a whole car |
| S3 | `engine_factory.py`             | Construction moves out of the car (trimmed to 1–2 methods) |
| S4 | `f1_car_v2.py`                  | The car gets its parts from factories                   |
| S5 | `test_engine_in_isolation.py`   | The engine is tested on its own                         |

**Takeaway:** the car uses its parts but doesn't build them.

## O: Open/Closed (4 gists)
**F1 story:** 1954. The rules switch to 2.5L naturally aspirated engines.

| #  | Gist                     | Shows                                                         |
|----|--------------------------|---------------------------------------------------------------|
| O1 | `f1_car_v3.py`           | Same class with one line edited to swap the engine (highlighted) |
| O2 | `f1_car_v4.py`           | Parts are passed in through the constructor                   |
| O3 | `build_f1_car_v4.py`     | Assembling the 1954 car                                       |
| O4 | `one_class_many_eras.py` | 1954, 1962 (monocoque) and 1977 (turbo + sidepods) cars built from the same `F1Car_v4`, with no history prose |

**Takeaway:** the class is closed for modification and open for extension. Add a "*mostly* open" caveat that sets up D.

## D: Dependency Inversion (7 gists)
**F1 story:** 1980s. The turbo engine ships with `start_with_turbocharger()` instead of `start()`.

| #  | Gist                        | Shows                                              |
|----|-----------------------------|----------------------------------------------------|
| D1 | `engine_1980s_turbo_v1.py`  | The new engine's API                               |
| D2 | `driver_v1_start_car.py`    | `Driver_v1` → `AttributeError`                     |
| D3 | `f1_car_v4_patched.py`      | A `type(engine) ==` switch. This is the code smell |
| D4 | `engine_interface.py`       | `EngineInterface` (ABC) as the contract            |
| D5 | `engine_1980s_turbo_v2.py`  | `TypeError` as soon as it's built                  |
| D6 | `engine_1980s_turbo_v3.py`  | Now matches the interface                          |
| D7 | `drive_turbo_car.py`        | `F1Car_v4` is unchanged and the car drives         |

**Aside (prose only):** ABC vs `typing.Protocol`. We use an ABC here because it fails when the object is built, not later on the track.

## L: Liskov Substitution (9 gists)
**F1 story:** 2014, the hybrid era. `HybridF1Car` replaces `F1CarWithTelemetry`. It subclasses it, so the substitution is literal.

**Setup**

| #  | Gist                          | Shows                                                                 |
|----|-------------------------------|-----------------------------------------------------------------------|
| L1 | `f1_car_with_telemetry.py`    | The base contract: starting without telemetry raises `TelemetryNotEnabledError`, every log is kept, any fuel amount is accepted, telemetry includes `"fuel"` |
| L2 | `hybrid_f1_car_v1.py`         | The naive hybrid port, which breaks all of the rules below            |
| L3 | `driver.py`                   | The code using the car. **It never changes in this section**          |

**Rule by rule.** Each one shows its symptom in the driver's code.

| #  | Rule                    | Symptom                                                                 |
|----|-------------------------|-------------------------------------------------------------------------|
| —  | Signature: methods      | Callback to D5: the ABC already catches a missing method (no new gist)  |
| L4 | Signature: exceptions   | `NotEnoughElectricityError` escapes from `push_accelerator`. The driver has never heard of it, so it crashes |
| L5 | Properties: invariant   | The telemetry-enabled check was dropped, so the car starts fine but `logs == []` |
| L6 | Properties: history     | Only the last 5 logs are kept, so `average_electricity_recovered` is wrong |
| L7 | Methods: precondition   | Fuel must be a multiple of 5, so `InvalidFuelAmountError`. The notebook has a slider |
| L8 | Methods: postcondition  | Telemetry drops `"fuel"`, so `average_fuel_usage` raises `KeyError`     |

**Fix**

| #  | Gist                  | Shows                                                                  |
|----|-----------------------|------------------------------------------------------------------------|
| L9 | `hybrid_f1_car_v2.py` | The contract is honoured inside the car: ERS skips boost when the battery is empty, fuel is rounded internally, full logs are kept, `"fuel"` is back. **The same `driver.py` drives both cars.** |

Close with a bullet list of rule → symptom → fix (Medium has no tables).

## I: Interface Segregation (6 gists)
**F1 story:** a heritage demo day. One driver takes out a 1950s car, a 1980s telemetry car and a 2014 hybrid.

| #  | Gist                         | Shows                                                               |
|----|------------------------------|---------------------------------------------------------------------|
| I1 | `f1_car_v1_forced_stubs.py`  | To satisfy the big `F1CarInterface`, the 1950s car has to stub out telemetry methods it doesn't have |
| I2 | `driver_capability_checks.py`| The driver wants boost on the hybrid, but the interface hides it, so `isinstance` checks spread through every method |
| I3 | `segregated_interfaces.py`   | `Startable`, `NonHybridAccelerable`, `HybridAccelerable`, `Telemetry` |
| I4 | `cars_declare_interfaces.py` | The three cars' class declarations, each taking only what it needs  |
| I5 | `focused_drivers.py`         | One driver for each set of capabilities                             |
| I6 | `driver_factory.py`          | Picks the driver from the car's interfaces. The checks live in one place instead of every method. The notebook has a car picker |

**Takeaway:** a new kind of car means a new interface and a new driver, and no existing code gets edited.

## Wrap-up (0 gists)
- How the principles depend on each other: S makes O possible, D makes O safe, L makes D trustworthy, I keeps L achievable.
- Links to the repo and the notebook.

**Total: 31 gists**

---

## Repo changes

- **`notebook.py` (marimo).** Follows the sections above.
  - Variable names are scoped to each section, because marimo doesn't allow the same name in two cells.
  - A `show_error()` helper shows the deliberate failures as callouts.
  - Interactive pieces: the fuel slider (L7) and the car picker (I6).
- **`app/`**
  - L refactor: `HybridF1Car_v1` (naive) and `_v2` (follows the contract). Both subclass `F1CarWithTelemetry`.
  - I refactor: `f1_car_v1_forced_stubs`, and drivers that check capabilities.
  - Bug fixes:
    - `DriverForNonHybridWithoutTelemetry.start_car` calls `car.start_engine(car)`.
    - `HybridF1CarWithTelemetry_v1` saves a bound method into telemetry instead of a value.
    - The hybrid driver rounds 10 up to 15.
    - `TelemetrySystemFactory` v2 and v3 are missing `@staticmethod`.
    - The notebook text has pre/postcondition backwards.
- **`snippets/`.** The source for every gist, one file each. A test runs every snippet that can run, so the gists always match working code.
- **`scripts/publish_gists.py` + `snippets/gists.json`.** Creates or updates the gists and saves their IDs, so re-running never duplicates. The 23 gists from 2023 are left alone.
- **Environment.**
  - Delete `env.yml` and the `.ipynb` (git history keeps them).
  - Add `pyproject.toml`, `uv.lock`, a PEP 723 header in `notebook.py`, `README.md`, and `tests/`.
- **`article/driving-change-solid-f1.md`.** Each gist URL goes on its own line so Medium embeds it.

## Order of work and checkpoints
1. Refactor `app/`, set up the environment, build the marimo notebook. **You review the notebook.**
2. Extract the snippets and run the tests. **You review the snippets.**
3. Publish the gists (public). **Waits for your go-ahead.**
4. Write the article with the gist URLs. **You review the article.**
5. Commit and push. **Waits for your go-ahead.**
