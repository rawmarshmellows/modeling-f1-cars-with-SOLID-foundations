# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.24",
# ]
# ///

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", app_title="Driving Change: SOLID F1")

with app.setup:
    import marimo as mo

    from app.chassis import ChassisFactory
    from app.drivers import DriverFactory
    from app.drivers.driver_v1 import Driver_v1
    from app.drivers.driver_v2 import Driver_v2
    from app.engine import EngineFactory
    from app.f1_cars.f1_car_v1 import F1Car_v1
    from app.f1_cars.f1_car_v4 import F1Car_v4
    from app.f1_cars.f1_car_v5 import F1Car_v5
    from app.f1_cars.f1_car_v7 import F1Car_v7
    from app.f1_cars.f1_car_with_telemetry_v1 import F1CarWithTelemetry_v1
    from app.f1_cars.f1_car_with_telemetry_v2 import F1CarWithTelemetry_v2
    from app.f1_cars.hybrid_f1_car_v1 import HybridF1Car_v1
    from app.f1_cars.hybrid_f1_car_v2 import HybridF1Car_v2
    from app.f1_cars.hybrid_f1_car_v3 import HybridF1Car_v3
    from app.fuel_tank import FuelTankFactory
    from app.garage import build_1950s_car, build_hybrid_car, build_telemetry_car
    from app.wheels import WheelsFactory
    from snippets.catalog import snippet_markdown


@app.function
def show_code(snippet_id):
    """Show a snippet exactly as it appears in the article and in its gist."""
    return mo.md(snippet_markdown(snippet_id))


@app.function
def outcome(action):
    """Run `action` and show the result, or the exception it raised, without halting the notebook."""
    try:
        result = action()
    except Exception as error:
        return mo.callout(mo.md(f"**{type(error).__name__}**\n\n```text\n{error}\n```"), kind="danger")
    return mo.callout(mo.md("No error raised" if result is None else str(result)), kind="success")


@app.function
def average_fuel_used_per_push(telemetry_logs):
    """Pit wall code, written against the promise in F1CarInterface.get_current_telemetry."""
    fuel = [log["fuel_in_milliliters"] for log in telemetry_logs]
    return (fuel[0] - fuel[-1]) / (len(fuel) - 1)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # 5 principles to stop your code from spinning out every time the rules change

    Formula One can't leave its rulebook alone, and neither can your product manager.

    **What if your code could shrug off rule changes the way a good F1 car does?**

    That's what SOLID is for. This notebook follows the article section by section, dragging a
    Python F1 car through seven decades of regulation changes. We take the corners in the order
    the code needs them, **S → O → D → L → I** (yes, SODLI), because Dependency Inversion hands
    out the interfaces that Liskov and Interface Segregation rely on.

    - Read-only code blocks are the exact snippets from the article (and its gists).
    - Code cells are live, so edit them, break a contract, and see what happens!
    - Deliberate crashes show up as red callouts, so the rest of the notebook keeps running.

    Lights out, and away we go!
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---
    ## S: Single Responsibility, or why your car shouldn't build its own engine

    > A class should have one, and only one, reason to change.

    **1951.** Alfa Romeo's 159 took Fangio to the title on a 1.5-litre supercharged engine that
    was fast, thirsty, and more or less permanently in pieces between races. Every rebuilt engine
    had to be tested before it went back in the car. **Here's our first car. Count its jobs:**
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.image(
        src=str(mo.notebook_dir() / "images" / "Alfa-Romeo-159-(1951).jpg"),
        width=480,
        rounded=True,
        caption="Alfa Romeo 159, 1951",
    )
    return


@app.cell(hide_code=True)
def _():
    show_code("S1")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    `F1Car_v1` *drives*, and it also *builds* every part it drives with. The knowledge of which
    engine the team runs lives inside the car, so testing that engine means building everything:
    """)
    return


@app.cell
def _():
    def _test_engine_starts():
        f1_car = F1Car_v1()  # only the car knows which engine to build, so we build the whole car
        f1_car.start_engine()
        assert f1_car.engine.has_started


    _test_engine_starts()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Construction and driving change for different reasons, so move construction into a
    factory whose only job is building engines (plus one each for chassis, wheels and fuel tank):
    """)
    return


@app.cell(hide_code=True)
def _():
    show_code("S3")
    return


@app.cell(hide_code=True)
def _():
    show_code("S4")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    The factory is now the one place that knows how the team builds its engines, so a test can
    use it with no car in sight:
    """)
    return


@app.cell
def _():
    def _test_engine_starts():
        engine = EngineFactory.create_engine_1950s_1_5L_supercharged_v1()  # built exactly as the car builds it
        engine.start()
        assert engine.has_started


    _test_engine_starts()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    In this section, we split building from driving: the car drives, the factory builds, and when
    an engine comes out wrong, you know exactly whose door to knock on.

    ---
    ## O: Open/Closed, or how to swap engines without opening up the car

    > Software entities should be open for extension, but closed for modification.

    **1954.** The regulations move to a 2.5-litre formula, and the teams go naturally aspirated.
    Thanks to our engine shop, the new engine is built and tested without a car. Lovely!
    **Now let's put it in the car:**
    """)
    return


@app.cell(hide_code=True)
def _():
    show_code("O1")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    One line, but it's inside the car, so every new engine means a new car class that has to
    be re-tested as a whole. Instead, let the car receive its parts through the constructor:
    """)
    return


@app.cell(hide_code=True)
def _():
    show_code("O2")
    return


@app.cell
def _():
    f1_car_1954 = F1Car_v4(
        engine=EngineFactory.create_engine_1950s_2_5L_naturally_aspirated_v1(),
        chassis=ChassisFactory.create_chassis_spaceframe_v1(),
        wheels=WheelsFactory.create_wheels_v1(),
        fuel_tank=FuelTankFactory.create_fuel_tank_v1(),
    )
    f1_car_1954.start_engine()
    f1_car_1954.engine.has_started
    return (f1_car_1954,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Then twenty-three years of innovation go by, and the car class never changes:
    """)
    return


@app.cell
def _(f1_car_1954):
    # 1962: Lotus 25 style, mid-rear engine in a monocoque chassis
    f1_car_1962 = F1Car_v4(
        engine=EngineFactory.create_engine_1960s_1_5L_naturally_aspirated_mid_rear_v1(),
        chassis=ChassisFactory.create_chassis_monocoque_v1(),
        wheels=WheelsFactory.create_wheels_v1(),
        fuel_tank=FuelTankFactory.create_fuel_tank_v1(),
    )

    # 1977: Renault RS01 turbo engine with Lotus 78 ground-effect sidepods
    f1_car_1977 = F1Car_v4(
        engine=EngineFactory.create_engine_1970s_1_5L_renault_rs01_v1(),
        chassis=ChassisFactory.create_chassis_monocoque_with_winged_sidepods_v1(),
        wheels=WheelsFactory.create_wheels_v1(),
        fuel_tank=FuelTankFactory.create_fuel_tank_v1(),
    )

    # Three eras, one class, zero edits to F1Car_v4
    [type(_car.engine).__name__ for _car in (f1_car_1954, f1_car_1962, f1_car_1977)]
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### 🛠️ Build your own car

    Pick any engine and chassis. `F1Car_v4` takes them all without an edit, *almost*. Try
    the **1980s turbo (v1)** engine before reading the next section.
    """)
    return


@app.cell
def _():
    engine_picker = mo.ui.dropdown(
        options={
            "1951 · 1.5L supercharged": EngineFactory.create_engine_1950s_1_5L_supercharged_v1,
            "1954 · 2.5L naturally aspirated": EngineFactory.create_engine_1950s_2_5L_naturally_aspirated_v1,
            "1962 · 1.5L mid-rear": EngineFactory.create_engine_1960s_1_5L_naturally_aspirated_mid_rear_v1,
            "1977 · Renault RS01 turbo": EngineFactory.create_engine_1970s_1_5L_renault_rs01_v1,
            "1980s · 1.5L turbo (v1)": EngineFactory.create_engine_1980s_1_5L_turbocharged_v1,
            "2014 · 1.6L hybrid turbo": EngineFactory.create_engine_2010s_1_6L_hybrid_turbocharged_v1,
        },
        value="1954 · 2.5L naturally aspirated",
        label="Engine",
    )
    chassis_picker = mo.ui.dropdown(
        options={
            "Spaceframe": ChassisFactory.create_chassis_spaceframe_v1,
            "Monocoque": ChassisFactory.create_chassis_monocoque_v1,
            "Monocoque with winged sidepods": ChassisFactory.create_chassis_monocoque_with_winged_sidepods_v1,
        },
        value="Spaceframe",
        label="Chassis",
    )
    mo.hstack([engine_picker, chassis_picker], justify="start")
    return chassis_picker, engine_picker


@app.cell
def _(chassis_picker, engine_picker):
    _car = F1Car_v4(
        engine=engine_picker.value(),
        chassis=chassis_picker.value(),
        wheels=WheelsFactory.create_wheels_v1(),
        fuel_tank=FuelTankFactory.create_fuel_tank_v1(),
    )


    def _start_and_push():
        with mo.capture_stdout() as radio:
            _car.start_engine()
            _car.push_accelerator(fuel_amount_in_milliliters=50)
        return f"`F1Car_v4` is running\n\n```text\n{radio.getvalue()}```"


    outcome(_start_and_push)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    In this section, we moved the choice of parts out of the car, so a new part no longer means a
    new car. Well... *almost* any part. Cue the ominous music.

    ---
    ## D: Dependency Inversion, or surviving an engine that starts differently

    > High-level modules should not depend on low-level modules. Both should depend on abstractions.

    **1986.** Every car on the grid runs a 1.5-litre turbo, and our supplier's shiny new one has
    a tiny change that absolutely nobody mentioned in the handover email: you start it with
    `start_with_turbocharger()`.
    """)
    return


@app.cell(hide_code=True)
def _():
    show_code("D1")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    `F1Car_v4` accepts any engine, so in it goes. `Driver_v1.start_car` just calls `car.start_engine()`:
    """)
    return


@app.cell
def _():
    turbo_car_v1 = F1Car_v4(
        engine=EngineFactory.create_engine_1980s_1_5L_turbocharged_v1(),
        chassis=ChassisFactory.create_chassis_monocoque_with_winged_sidepods_v1(),
        wheels=WheelsFactory.create_wheels_v1(),
        fuel_tank=FuelTankFactory.create_fuel_tank_v1(),
    )
    outcome(lambda: Driver_v1().start_car(turbo_car_v1))
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    The car quietly depends on every engine having `start()`, and nothing enforces it. The
    tempting race-day patch teaches the car about each engine, undoes Open/Closed, and silently
    does nothing for any engine it doesn't recognise:
    """)
    return


@app.cell(hide_code=True)
def _():
    show_code("D3")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Dependency Inversion flips the arrow. The car team writes down what it needs from an engine,
    in its own package (`app/f1_cars/`), and **both sides depend on that abstraction**. The team's
    own engines already fit and sign up with one line; the supplier's turbo signs up too:
    """)
    return


@app.cell(hide_code=True)
def _():
    show_code("D4")
    return


@app.cell(hide_code=True)
def _():
    show_code("D5")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    The engine signed the contract but still has no `start()`. The mistake that crashed on
    the grid now fails in the factory:
    """)
    return


@app.cell
def _():
    outcome(EngineFactory.create_engine_1980s_1_5L_turbocharged_v2)
    return


@app.cell(hide_code=True)
def _():
    show_code("D7")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Last, the car names what it depends on. The only change is a type annotation, which also lets
    a type checker reject an engine that never signed the contract, before anything runs:
    """)
    return


@app.cell(hide_code=True)
def _():
    show_code("D8")
    return


@app.cell
def _():
    turbo_car_v3 = F1Car_v5(
        engine=EngineFactory.create_engine_1980s_1_5L_turbocharged_v3(),
        chassis=ChassisFactory.create_chassis_monocoque_with_winged_sidepods_v1(),
        wheels=WheelsFactory.create_wheels_v1(),
        fuel_tank=FuelTankFactory.create_fuel_tank_v1(),
    )
    Driver_v1().start_car(turbo_car_v3)  # the same Driver_v1, and a car that never learned about turbos
    turbo_car_v3.engine.has_started
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    In this section, we flipped the dependency so the car and the engines both depend on a
    contract. The ABC turns away an engine that signs but doesn't deliver, and a type checker
    rejects one that never signed at all.

    /// admonition | ABC or `typing.Protocol`?
    A `Protocol` describes the same contract structurally, with no subclassing, and a type
    checker enforces it before the code runs. An ABC is enforced at runtime, when the object
    is created. We use ABCs because watching the factory refuse a broken engine is the lesson.
    ///

    ---
    ## L: Liskov Substitution, or how a hybrid quietly broke everyone's code

    > If S is a subtype of T, then objects of type T may be replaced with objects of type S
    > without altering any of the desirable properties of the program.

    In plain English: if your code works with a class, it should keep working when you hand it a
    subclass. No surprises, and no "well, *technically* it's still a car". Liskov and Wing break
    that down into three rules:

    1. **Signature rule:** implement every method with compatible types, and raise no new exceptions.
    2. **Properties rule:** keep the parent's invariants and history.
    3. **Methods rule:** don't strengthen preconditions or weaken postconditions.

    Python checks very little of this: an ABC checks that methods exist, a type checker checks
    signatures, and nothing checks the rest. By the late 1980s the car has telemetry and an
    interface whose docstrings make promises, including an invariant and a history:
    """)
    return


@app.cell(hide_code=True)
def _():
    show_code("L1")
    return


@app.cell(hide_code=True)
def _():
    show_code("L2")
    return


@app.cell(hide_code=True)
def _():
    show_code("L3")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    **2014.** The hybrid era: a 1.6-litre turbo, a battery, and an energy recovery system whose
    MGU-H turns exhaust heat into electricity that can be deployed as a boost. The hybrid subclasses the telemetry car, and it was ported in a hurry:
    """)
    return


@app.cell(hide_code=True)
def _():
    show_code("L4")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Signature rule: no new exceptions

    The battery leaves the garage flat, and the hybrid boosts on every push:
    """)
    return


@app.cell
def _():
    def _drive_flat_battery_hybrid():
        hybrid = build_hybrid_car(HybridF1Car_v1)  # the battery leaves the garage flat
        driver = Driver_v2()
        driver.start_car(hybrid)
        driver.accelerate_car(hybrid, fuel_amount_in_milliliters=50)


    outcome(_drive_flat_battery_hybrid)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Properties rule: keep the invariants

    Charge the battery. No crash, but the car never refuses to start, so the driver never
    enables telemetry, and the engine runs unrecorded:
    """)
    return


@app.cell
def _():
    _hybrid = build_hybrid_car(HybridF1Car_v1, battery_charge_in_kilojoules=4_000)
    _driver = Driver_v2()
    _driver.start_car(_hybrid)  # no TelemetryNotEnabledError, so the driver never enables telemetry
    _driver.accelerate_car(_hybrid, fuel_amount_in_milliliters=50)
    {
        "engine running": _hybrid.engine.has_started,
        "telemetry recording": _hybrid.telemetry_system.is_enabled,
        "telemetry logs": _hybrid.get_telemetry_logs(),
    }
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Properties rule: keep the history

    The log should only grow. Enable telemetry by hand, push once and note the first snapshot,
    then push nine more times:
    """)
    return


@app.cell
def _():
    _hybrid = build_hybrid_car(HybridF1Car_v1, battery_charge_in_kilojoules=4_000)
    _driver = Driver_v2()
    _driver.start_car(_hybrid)
    _hybrid.enable_telemetry()  # enable it by hand this time
    _driver.accelerate_car(_hybrid, fuel_amount_in_milliliters=50)
    _first_snapshot = _hybrid.get_telemetry_logs()[0]
    for _ in range(9):
        _driver.accelerate_car(_hybrid, fuel_amount_in_milliliters=50)

    {
        "first snapshot still in the log": _first_snapshot in _hybrid.get_telemetry_logs(),
        "snapshots reported": len(_hybrid.get_telemetry_logs()),
    }
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Methods rule: don't strengthen preconditions

    The parent accepts any amount of fuel. Slide the amount and compare the hurried hybrid
    with the fixed one (`HybridF1Car_v2`, shown further down):
    """)
    return


@app.cell
def _():
    fuel_per_push = mo.ui.slider(start=1, stop=20, value=8, label="Fuel per push (mL)", show_value=True)
    fuel_per_push
    return (fuel_per_push,)


@app.cell
def _(fuel_per_push):
    def _push(car_class):
        car = build_hybrid_car(car_class, battery_charge_in_kilojoules=4_000)
        driver = Driver_v2()
        car.enable_telemetry()
        driver.start_car(car)
        driver.accelerate_car(car, fuel_amount_in_milliliters=fuel_per_push.value)
        return f"Drew {fuel_per_push.value}mL from the tank, {car.fuel_tank.current_fuel_in_tank.amount_in_milliliters}mL left"


    mo.hstack(
        [
            mo.vstack([mo.md("**`HybridF1Car_v1`**"), outcome(lambda: _push(HybridF1Car_v1))]),
            mo.vstack([mo.md("**`HybridF1Car_v2`**"), outcome(lambda: _push(HybridF1Car_v2))]),
        ],
        widths="equal",
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Methods rule: don't weaken postconditions

    `average_fuel_used_per_push` (defined at the top of this notebook) relies on every snapshot
    including `fuel_in_milliliters`:
    """)
    return


@app.cell
def _():
    _hybrid = build_hybrid_car(HybridF1Car_v1, battery_charge_in_kilojoules=4_000)
    _hybrid.enable_telemetry()
    _driver = Driver_v2()
    _driver.start_car(_hybrid)
    for _ in range(10):
        _driver.accelerate_car(_hybrid, fuel_amount_in_milliliters=50)

    outcome(lambda: average_fuel_used_per_push(_hybrid.get_telemetry_logs()))
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### The fix: keep the promises inside the subtype

    Don't patch every caller. The hybrid made the promises when it subclassed the telemetry
    car, so the hybrid keeps them:
    """)
    return


@app.cell(hide_code=True)
def _():
    show_code("L10")
    return


@app.cell
def _():
    _cars = [
        build_telemetry_car(F1CarWithTelemetry_v1),
        build_hybrid_car(HybridF1Car_v2),  # flat battery again
    ]
    _driver = Driver_v2()  # not a single line of the driver has changed
    for _car in _cars:
        _driver.start_car(_car)
        for _ in range(10):
            _driver.accelerate_car(_car, fuel_amount_in_milliliters=8)

    {
        "telemetry logs": [len(_car.get_telemetry_logs()) for _car in _cars],
        "average fuel per push": [average_fuel_used_per_push(_car.get_telemetry_logs()) for _car in _cars],
    }
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    In this section, the rushed hybrid ran fine on its own; it was everyone relying on its contract
    who ended up in the gravel. Tools can check that methods exist and signatures line up, but
    everything else lives in docstrings and tests, and a subclass has to honour those too.

    ---
    ## I: Interface Segregation, or one driver and three generations of car

    > Clients should not be forced to depend on methods they do not use.

    **Heritage demo day.** One driver, three generations of car, one very long afternoon: a 1950s
    car, the 1980s telemetry car and the 2014 hybrid. A 1950s car can't implement `F1CarInterface`
    with a straight face:
    """)
    return


@app.cell(hide_code=True)
def _():
    show_code("I1")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    And the driver who wants the hybrid's boost has to check concrete classes:
    """)
    return


@app.cell(hide_code=True)
def _():
    show_code("I2")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    The interface is too big (three capabilities not every car has) and too small (no way to say
    a car can boost). Split it into one interface per capability, add the missing one, and let
    each car sign up for what it can actually do. `StartableInterface` documents `StartRefusedError`,
    and `TelemetryNotEnabledError` subclasses it, so telemetry cars stay honest `Startable`s:
    """)
    return


@app.cell(hide_code=True)
def _():
    show_code("I3")
    return


@app.cell(hide_code=True)
def _():
    show_code("I4")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Drivers are written per set of capabilities, and a factory picks one by asking about
    interfaces rather than concrete classes:
    """)
    return


@app.cell(hide_code=True)
def _():
    show_code("I5")
    return


@app.cell(hide_code=True)
def _():
    show_code("I6")
    return


@app.cell
def _():
    _heritage_cars = [
        build_1950s_car(F1Car_v7),
        build_telemetry_car(F1CarWithTelemetry_v2),
        build_hybrid_car(HybridF1Car_v3, battery_charge_in_kilojoules=4_000),
    ]
    for _car in _heritage_cars:
        _driver = DriverFactory.create_driver_for(_car)
        _driver.start_car(_car)
        _driver.accelerate_car(_car, fuel_amount_in_milliliters=50)
        _driver.overtake(_car, fuel_amount_in_milliliters=100)

    [type(DriverFactory.create_driver_for(_car)).__name__ for _car in _heritage_cars]
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### 🏁 Take a car out

    Pick a car, and `DriverFactory` picks the driver. The team radio shows what happened.
    """)
    return


@app.cell
def _():
    car_picker = mo.ui.dropdown(
        options={
            "1950s car · F1Car_v7": lambda: build_1950s_car(F1Car_v7),
            "1980s telemetry car · F1CarWithTelemetry_v2": lambda: build_telemetry_car(F1CarWithTelemetry_v2),
            "2014 hybrid · HybridF1Car_v3": lambda: build_hybrid_car(HybridF1Car_v3, battery_charge_in_kilojoules=4_000),
        },
        value="2014 hybrid · HybridF1Car_v3",
        label="Heritage car",
    )
    car_picker
    return (car_picker,)


@app.cell
def _(car_picker):
    _car = car_picker.value()
    _driver = DriverFactory.create_driver_for(_car)
    with mo.capture_stdout() as _radio:
        _driver.start_car(_car)
        _driver.accelerate_car(_car, fuel_amount_in_milliliters=50)
        _driver.overtake(_car, fuel_amount_in_milliliters=100)

    mo.vstack(
        [
            mo.md(f"`DriverFactory` picked **`{type(_driver).__name__}`**"),
            mo.plain_text(_radio.getvalue()),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    In this section, we split one bloated interface into small ones, so every car keeps its promises
    honestly. The trade-off: a genuinely new *combination* of capabilities still needs a new driver
    and one branch in `DriverFactory`, but that's a small edit in one place, against abstractions.

    ---
    ## Conclusion

    Thanks for playing along, and hopefully, SOLID has clicked! Each fix made the next one possible:

    - **Single Responsibility** took construction out of the car, which let us hand the car its parts.
    - **Open/Closed** let the car take any part without being edited, but "any part" was an unchecked assumption.
    - **Dependency Inversion** turned the assumption into a contract, and moved the failure from the grid to the factory, or the type checker.
    - **Liskov Substitution** made the contract mean something: subtypes keep the promises, not just the signatures.
    - **Interface Segregation** kept contracts small enough for every car to keep honestly.

    F1 teams don't win by predicting next season's rules; they win by building cars that can take
    whatever the rulebook throws at them. Now go break a contract and see who ends up in the barriers!
    """)
    return


if __name__ == "__main__":
    app.run()
