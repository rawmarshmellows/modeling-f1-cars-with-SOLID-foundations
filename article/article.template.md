# Driving Change: SOLID Principles in Python, Told Through an F1 Car

*Five principles, five refactors, and just enough Formula One to keep it moving.*

Formula One rewrites its rulebook almost every season. Engines change size, chassis change shape, and whole technologies arrive or get banned overnight. A team whose car can't absorb those changes doesn't win.

Software has the same problem under a less glamorous name: changing requirements. SOLID is five principles for writing code that survives them:

- **S**ingle Responsibility
- **O**pen/Closed
- **L**iskov Substitution
- **I**nterface Segregation
- **D**ependency Inversion

In this article we'll build a Python model of an F1 car and evolve it through seven decades of regulation changes. Each principle gets one moment from F1 history for context, and the rest is code: what broke, why it broke, and the refactor that fixed it. We'll go in the order the code needs them, S → O → D → L → I, because Dependency Inversion introduces the interfaces that Liskov and Interface Segregation build on.

Every snippet below is a real file from the companion repo, and the repo's test suite checks every one of them, so what you read is what runs. To follow along:

```bash
git clone https://github.com/rawmarshmellows/modeling-f1-cars-with-SOLID-foundations
cd modeling-f1-cars-with-SOLID-foundations
uv run marimo edit notebook.py
```

---

## S: The Single Responsibility Principle

> A class should have one, and only one, reason to change.

**1951.** Alfa Romeo's 159 took Juan Manuel Fangio to the world title with a 1.5-litre supercharged engine: fast, thirsty, and in need of constant work between races. Every time an engine was reworked, it had to be tested before it went back in the car.

Here's our first car. Look at what it's responsible for:

{{gist:S1}}

`F1Car_v1` does two jobs. It *drives* (start, stop, push the accelerator), and it *builds* every part it drives with. Because of that second job, the knowledge of *which* engine the team runs, and how it's put together, lives inside the car. Testing the engine the car actually uses looks like this:

{{gist:S2}}

To check that the engine starts, we build a chassis, wheels and a full fuel tank. Worse, when the team changes how its engines are built, the class we have to open up is the car, even though nothing about driving changed. That's two reasons to change in one class.

The fix is to move construction into a class whose only job is building engines:

{{gist:S3}}

The repo's `EngineFactory` has one `create_…` method per engine; this excerpt shows the first. Chassis, wheels and the fuel tank get factories too, and the car now asks for its parts instead of building them:

{{gist:S4}}

The factory is now the one place that knows how the team builds its engines. The car uses it, and so can a test, with no car in sight:

{{gist:S5}}

**Takeaway:** the car uses its parts; it doesn't build them. Construction and driving change for different reasons, so they live in different classes, and a problem building an engine now stays in the factory.

---

## O: The Open/Closed Principle

> Software entities should be open for extension, but closed for modification.

**1954.** The regulations moved to a 2.5-litre formula, and the teams answered with naturally aspirated engines. Thanks to the factory, the new engine was built and tested in isolation. Then it had to go into the car:

{{gist:O1}}

The whole change is one line. But that line is inside the car class, so we get a new car class, `F1Car_v3`, which has to be tested all over again even though its chassis, wheels and tank haven't changed. And every future engine means editing the car again. The only way to extend the car is to modify it.

The fix is to stop the car from choosing its parts at all. It receives them through its constructor:

{{gist:O2}}

Whoever assembles the car picks the parts:

{{gist:O3}}

Now fast-forward through the next twenty-three years of innovation: mid-rear engines, the monocoque chassis, turbocharging and ground-effect sidepods.

{{gist:O4}}

Three eras, one class, zero edits. `F1Car_v4` is **closed for modification**, because nothing inside it changes, and **open for extension**, because any new part can go in. Well, *almost* any part. The next section shows what happens when a part doesn't behave the way the car assumes.

---

## D: The Dependency Inversion Principle

> High-level modules should not depend on low-level modules. Both should depend on abstractions.

**1986.** Renault's turbo gamble had become the standard, and every car on the grid ran a 1.5-litre turbo. Our supplier's new turbo engine came with one small difference that nobody mentioned: you start it with `start_with_turbocharger()` instead of `start()`.

{{gist:D1}}

`F1Car_v4` accepts any engine, so in it goes. Then the driver tries to start the car. `Driver_v1.start_car` just calls `car.start_engine()`:

{{gist:D2}}

The Open/Closed win had a hidden assumption. The car accepts *any* engine, but it quietly depends on every engine having a `start()` method, and nothing enforces that. We only find out on the grid.

Under race-day pressure, the tempting fix is to teach the car about each engine:

{{gist:D3}}

It works, but it undoes everything the last section achieved. The car imports concrete engine classes again, has to be edited for every new one, and silently does nothing for any engine it doesn't recognise, including the 1962 and 1977 engines from the last section. The root cause is the direction of the dependency: the high-level car depends on low-level engines.

Dependency Inversion flips that. The car team writes down what it needs from an engine, and **both sides depend on that abstraction**:

{{gist:D4}}

Python has no `interface` keyword; an abstract base class (ABC) is the closest equivalent. Notice where it lives: in `app/f1_cars/`, the car team's package. The engines import it from there, so the low-level parts now depend on something the high-level car owns. That's the inversion. The team's own engines already had these four methods, so each one signed up with a one-line change. The supplier's turbo signs up the same way:

{{gist:D5}}

It still has no `start()` method. Here's what happens now:

{{gist:D6}}

That's the point. The mistake that used to crash on the grid now fails the moment the engine is built, inside the factory, long before it reaches a car. To pass, the engine implements what the contract asks for:

{{gist:D7}}

Last, the car says out loud what it depends on. The only change is a type annotation:

{{gist:D8}}

The car still knows nothing about turbos, and the driver from before is untouched:

{{gist:D9}}

**Takeaway:** `F1Car_v5` doesn't know or care which engine it has. It names `EngineInterface` as the thing it needs, and every engine that wants to go in the car implements it. The dependency that used to point from car to engine now points from both of them to the contract. Two safety nets come with it: the ABC refuses an engine that signs the contract but doesn't deliver, the moment it's built, and a type checker such as mypy rejects an engine that never signed it, like the original turbo, before the code even runs.

> **ABC or `typing.Protocol`?** A `Protocol` describes the same contract structurally, with no subclassing (the engines wouldn't even need to import it), and a type checker such as mypy or pyright enforces it before the code runs. An ABC is enforced at runtime, when the object is created. We use ABCs here because watching the factory refuse a broken engine is the lesson, but in a type-checked codebase a `Protocol` is often the lighter option.

---

## L: The Liskov Substitution Principle

> If S is a subtype of T, then objects of type T may be replaced with objects of type S without altering any of the desirable properties of the program.

In plainer terms: anywhere your code uses a class, you should be able to hand it a subclass and nothing should break. Barbara Liskov and Jeannette Wing split that promise into three rules:

1. **The signature rule:** a subtype implements every method with compatible argument and return types, and raises no new exceptions.
2. **The properties rule:** a subtype keeps its parent's invariants and its history.
3. **The methods rule:** a subtype can't strengthen preconditions or weaken postconditions.

Python checks very little of this. An ABC checks that the methods exist, a type checker checks their signatures, and nothing checks the rest. Let's see what that costs.

By the late 1980s our car has telemetry, and after the turbo incident the team gave the car an interface of its own. This time the contract isn't just method signatures. The docstrings make promises too, including an invariant and a promise about the history of the logs:

{{gist:L1}}

The 1980s telemetry car keeps every one of those promises. Note that `disable_telemetry` stops the engine first, so the invariant holds whichever order things happen in:

{{gist:L2}}

And the driver is written against the contract. It handles `TelemetryNotEnabledError` because the interface says that error can happen:

{{gist:L3}}

**2014.** The hybrid era arrives: a 1.6-litre turbo engine, a battery, and an energy recovery system whose MGU-H turns exhaust heat into electricity that can be deployed as a boost. A hybrid is a telemetry car with extra hardware, so it subclasses `F1CarWithTelemetry_v1`. It was ported in a hurry:

{{gist:L4}}

Each change comes with a reasonable-sounding comment, and each one breaks the contract. Let's hand it to the unchanged `Driver_v2` and go through them one rule at a time.

### Signature rule: no new exceptions

Part of the signature rule has tooling behind it. An ABC catches a *missing* method (we watched one refuse to build an incomplete engine back in D6), and a type checker catches an override with incompatible arguments. Nothing catches a new exception:

{{gist:L5}}

The hybrid deploys its boost on every push, and its battery leaves the garage flat. `NotEnoughElectricityError` is an exception the parent never raises, so a driver who handles exactly what the interface documents crashes.

### Properties rule: keep the invariants

Charge the battery and try again:

{{gist:L6}}

No crash, and no data. The interface's invariant says the engine only runs while telemetry is recording, and `Driver_v2` relies on it: the driver switches telemetry on *when the car refuses to start*. The hybrid dropped the check, so the car starts, the engine runs unrecorded, and telemetry never gets switched on. No exception, no warning, just an empty list on the pit wall.

### Properties rule: keep the history

Enable telemetry by hand this time. Push once and note the first snapshot, then push nine more times:

{{gist:L7}}

The interface promised that the log only grows, and that a snapshot, once recorded, never disappears. The hybrid still records every snapshot but only reports the last five, so a snapshot the pit wall has already seen vanishes. Anything that counts, totals or replays the logs is now silently wrong.

### Methods rule: don't strengthen preconditions

{{gist:L8}}

The parent accepts any amount of fuel. The hybrid's injector only takes multiples of 5 mL, and the car passes that restriction straight on to its callers. It shows up as yet another new exception, so it overlaps the signature rule, but the cause is different: the method now demands more of whoever calls it. Code that was correct yesterday is wrong today, and none of it changed.

### Methods rule: don't weaken postconditions

{{gist:L9}}

`get_current_telemetry` promised a snapshot that *always* includes `fuel_in_milliliters`. The hybrid swapped fuel for electricity, so code written against the promise gets a `KeyError`.

### The fix: keep the promises inside the subtype

Look at what we *didn't* do: patch `Driver_v2` with a new `except` for every new error and an `if` for every new quirk. That would spread the hybrid's problems into every piece of code that uses a car. The hybrid made those promises the moment it subclassed `F1CarWithTelemetry_v1`, so the hybrid is where they get kept:

{{gist:L10}}

- **New exception:** a flat battery now means no boost, not a crash, and fuel is drawn before anything else can go wrong.
- **Invariant:** `start_engine` is inherited, so the telemetry check is back.
- **History:** `get_telemetry_logs` is inherited, so every log is kept.
- **Precondition:** any amount of fuel is accepted. The car draws exactly what was asked from the tank, the injector burns it in 5 mL pulses, and any remainder waits in the fuel line for the next push.
- **Postcondition:** the snapshot contains everything the parent's did, *plus* the battery.

And the proof:

{{gist:L11}}

The same driver and the same pit wall code, given both cars, produce identical results. That's substitutability.

**Takeaway:** Single Responsibility, Open/Closed and Dependency Inversion are about how code is structured. Liskov is about the code that *uses* it. The hurried hybrid worked fine on its own terms, and it was everyone relying on the contract who broke. Tools can check that a contract's methods exist and that their signatures line up. Everything else lives in docstrings and tests, and a subclass has to honour those too.

---

## I: The Interface Segregation Principle

> Clients should not be forced to depend on methods they do not use.

**Heritage demo day.** The team takes three generations of car to a festival: a 1950s car, the 1980s telemetry car and the 2014 hybrid. One driver drives all three.

The only car abstraction we have is `F1CarInterface`, and a 1950s car can't honestly implement it:

{{gist:I1}}

The interface forces four telemetry methods onto a car that has no telemetry, and every stub is a lie. `get_telemetry_logs` returning `[]` looks exactly like the broken invariant from the Liskov section, and `get_current_telemetry` breaks the promise to always include fuel. It can't keep the invariant either, because its engine runs with nothing recording it. A bloated interface doesn't just add boilerplate; it makes Liskov violations unavoidable.

The driver has the opposite problem. On demo day they want to use the hybrid's boost to overtake, but `F1CarInterface` has no concept of boost, so the driver has to work out which car it's holding:

{{gist:I2}}

Those `isinstance` checks name a concrete class. That's the Dependency Inversion problem from the turbo section all over again, and the Open/Closed one too: a `HybridF1Car_v3`, or next year's car, means editing the driver.

So the interface is both too big and too small. It bundles three capabilities (starting, accelerating and telemetry) that not every car has, and it has no way to say that a car can boost. Split it into one interface per capability, and add the missing one:

{{gist:I3}}

Look closely at `StartableInterface`: it documents that a car may refuse to start with `StartRefusedError`. Telemetry cars refuse with `TelemetryNotEnabledError`, which subclasses it, so a telemetry car is still an honest `Startable`. Splitting interfaces mustn't sneak the new-exception violation back in.

Each car signs up for exactly what it can do. The class bodies are elided here; the full classes are in the repo:

{{gist:I4}}

The 1950s car no longer has to pretend, and the hybrid can say plainly that it's boostable. Now drivers can be written for a set of capabilities:

{{gist:I5}}

`DriverForBasicCar` handles `StartRefusedError` because `StartableInterface` says it can happen, so even handed a telemetry car it reports the refusal instead of crashing. `DriverForHybridCar` calls `enable_boost()` because every car it's given promises `BoostableInterface`, with no `isinstance` and no guessing. The drivers deliberately don't inherit from one another: a hybrid driver needs a boostable car, which is a *stronger precondition* than a basic driver has, and that's exactly what Liskov says a subclass can't impose.

Something still has to match drivers to cars. That decision now lives in one place, and it asks about capabilities rather than concrete classes:

{{gist:I6}}

Demo day:

{{gist:I7}}

**Takeaway:** a new kind of car implements the interfaces it needs, and the existing drivers work with it. There is a trade-off: a genuinely new *combination* of capabilities needs a new driver and one new branch in `DriverFactory`. That's still an edit, but a small one in a single place, and it checks abstractions instead of scattering `isinstance` checks against concrete classes through every method of every driver.

---

## Wrap-up: the principles hold each other up

Five principles, one story, and each fix made the next one possible:

- **Single Responsibility** took construction out of the car, which is what let us hand the car its parts.
- **Open/Closed** let the car take any part without being edited, but "any part" was an unchecked assumption.
- **Dependency Inversion** turned that assumption into a contract both sides depend on, and moved the failure from the grid to the factory, or to the type checker.
- **Liskov Substitution** made sure the contract means something: a subtype keeps the promises, not just the signatures.
- **Interface Segregation** kept the contracts small enough that every car could keep them honestly.

F1 teams don't win by predicting next season's regulations. They win by building cars that can absorb them. SOLID won't predict your next requirement either, but it turns that requirement into a new class instead of a rewrite.

All the code, the tests that check every snippet in this article, and an interactive marimo notebook are on GitHub at [rawmarshmellows/modeling-f1-cars-with-SOLID-foundations](https://github.com/rawmarshmellows/modeling-f1-cars-with-SOLID-foundations). Clone it, break a contract, and see what happens.
