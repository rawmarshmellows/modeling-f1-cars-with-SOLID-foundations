# 5 principles to stop your code from spinning out every time the rules change

*Let SOLID help you build a Python F1 car that survives 70 years of regulation changes*

Formula One can't leave its rulebook alone. Engines shrink, grow, sprout turbos, and lose them again. Entire technologies get invented in February and banned by August. The teams that win aren't the ones who predict the new rules; they're the ones whose cars can take a rule change without being rebuilt from scratch.

Sound familiar? Swap "the FIA" for "your product manager" and "new regulations" for "just one small change to the requirements", and congratulations, you're an F1 engineer (minus the champagne).

**What if your code could shrug off rule changes the way a good F1 car does?**

That's what the SOLID principles are for. This article will show how we can use them to drag a Python model of an F1 car through seven decades of F1 history:

- **S**ingle Responsibility: stop the car from building its own engine
- **O**pen/Closed: swap engines without opening up the car
- **D**ependency Inversion: survive an engine that starts differently
- **L**iskov Substitution: stop a hybrid from quietly breaking everyone's code
- **I**nterface Segregation: let one driver drive a 1950s car and a 2014 hybrid on the same afternoon

Yes, that spells SODLI. We take the corners in the order the code needs them, because Dependency Inversion hands out the interfaces that Liskov and Interface Segregation rely on. Sorry, acronym fans.

Each principle gets exactly one moment of F1 history, and after that it's code all the way down: what broke, why it broke, and how we fixed it. Hopefully, by the end of this article, SOLID will feel less like a job-interview acronym and more like something you actually reach for!

Every snippet below is a real file from the companion repo, and the test suite runs every single one of them, so nothing here only works on slides. If you'd rather poke at the code than read about it, everything is self-contained, so there's no setup beyond:

```bash
git clone https://github.com/rawmarshmellows/modeling-f1-cars-with-SOLID-foundations
cd modeling-f1-cars-with-SOLID-foundations
uv run marimo edit notebook.py
```

That opens an interactive marimo notebook that follows this article section by section, so you can break things on purpose.

Lights out, and away we go!

---

## S: Single Responsibility, or why your car shouldn't build its own engine

> A class should have one, and only one, reason to change.

**1951.** Alfa Romeo's 159 carried Juan Manuel Fangio to the world title on a 1.5-litre supercharged engine that was fast, thirsty, and more or less permanently in pieces between races. Every rebuilt engine had to be tested before it went back into the car.

**Here's our first car. Count its jobs:**

{{gist:S1}}

Two! `F1Car_v1` *drives* (start, stop, push the accelerator), and it also *builds* every part it drives with. It's the racing driver who insists on machining their own pistons. Because of that second job, the knowledge of *which* engine the team runs, and how it's put together, lives inside the car.

**Let's test the engine:**

{{gist:S2}}

To check that one engine starts, we assemble an entire car: chassis, wheels, and 140 litres of fuel. Worse, when the engine shop changes how engines are built, the file they have to open is the car, even though nothing about driving has changed. That's two reasons to change in one class.

**Let's hire an engine shop, a class whose only job is building engines:**

{{gist:S3}}

The real `EngineFactory` has one `create_…` method per engine; this excerpt shows the first. The chassis, wheels, and fuel tank get their own shops too, so the car can go back to doing what it's good at:

{{gist:S4}}

The factory is now the one place that knows how the team builds its engines. The car uses it, and so can a test, with no car anywhere in sight:

{{gist:S5}}

In this section, we split building from driving: the car drives, the factory builds, and when an engine comes out wrong, you know exactly whose door to knock on. In the next section, we'll see what happens when the rulebook demands a brand-new engine.

---

## O: Open/Closed, or how to swap engines without opening up the car

> Software entities should be open for extension, but closed for modification.

**1954.** The regulations move to a 2.5-litre formula, and the teams go naturally aspirated. Thanks to our engine shop, the new engine is built and tested without a car in sight. Lovely!

**Now let's put it in the car:**

{{gist:O1}}

One line. What could possibly go wrong? Well, that line lives inside the car, so "new engine" means "new car class". `F1Car_v3` needs testing from scratch even though its chassis, wheels, and tank are identical, and next season's engine means doing it all over again. The only way to extend this car is to take a spanner to it.

**Let's stop the car from picking its own parts, and hand them over through the constructor instead:**

{{gist:O2}}

Now whoever assembles the car decides what goes into it:

{{gist:O3}}

**Let's fast-forward through twenty-three years of wild innovation** (mid-rear engines, monocoque chassis, turbos, and ground-effect sidepods) and count how many times we have to edit the car class:

{{gist:O4}}

Zero! Three eras, one class. `F1Car_v4` is **closed for modification** because nothing inside it changes, and **open for extension** because any part bolts right on.

In this section, we moved the choice of parts out of the car, so a new part no longer means a new car. Well... *almost* any part. In the next section, an engine turns up that doesn't behave the way the car assumes. Cue the ominous music.

---

## D: Dependency Inversion, or surviving an engine that starts differently

> High-level modules should not depend on low-level modules. Both should depend on abstractions.

**1986.** Renault's turbo gamble has taken over the sport, and every car on the grid runs a 1.5-litre turbo. Our supplier delivers a shiny new one, with one tiny change that absolutely nobody mentioned in the handover email: you start it with `start_with_turbocharger()` instead of `start()`.

{{gist:D1}}

`F1Car_v4` takes any engine, so in it goes. **Let's start the car.** `Driver_v1.start_car` simply calls `car.start_engine()`:

{{gist:D2}}

Silence on the grid. It turns out our Open/Closed win came with some small print: the car accepts *any* engine, but it quietly assumes every engine has a `start()` method, and nothing checks.

It's race day, so somebody reaches for the quick fix and teaches the car about each engine:

{{gist:D3}}

It works! It also undoes everything the last section achieved. The car imports concrete engine classes again, needs editing for every new one, and silently does nothing for any engine it doesn't recognise, including the 1962 and 1977 engines we were so proud of five minutes ago. The real problem is which way the dependency points: the high-level car depends on low-level engines.

Dependency Inversion turns that around. **Let's have the car team write down what it needs from an engine, so both sides depend on that abstraction instead:**

{{gist:D4}}

Let's break this down:

- Python has no `interface` keyword, so an abstract base class (ABC) does the job.
- It lives in `app/f1_cars/`, the car team's package. The engines import it from there, so the low-level parts now depend on something the high-level car owns. That's the "inversion"!
- The team's own engines already had these four methods, so each one signed up with a one-line change.

**The supplier's turbo signs up too:**

{{gist:D5}}

It signed, but it still doesn't have a `start()` method. **Let's see how that goes:**

{{gist:D6}}

This is the good kind of failure. The mistake that used to strand us on the grid now blows up the moment the engine is built, back at the factory, long before it gets anywhere near a car. To pass inspection, the engine has to deliver what it signed up for:

{{gist:D7}}

**Finally, let's have the car say out loud what it depends on.** The whole change is one type annotation:

{{gist:D8}}

The car still knows nothing about turbos and the driver hasn't changed, but this time the engine fires up:

{{gist:D9}}

`F1Car_v5` doesn't know or care which engine it has. It names `EngineInterface` as the thing it needs, and every engine that wants a seat implements it. We also get two safety nets thrown in for free:

- The ABC rejects an engine that signs the contract but doesn't deliver, the moment it's built.
- A type checker such as mypy rejects an engine that never signed at all, like our original turbo, before the code even runs.

> **ABC or `typing.Protocol`?** A `Protocol` describes the same contract structurally, with no subclassing (the engines wouldn't even need to import it), and a type checker such as mypy or pyright enforces it before the code runs. An ABC is enforced at runtime, when the object is created. We're using ABCs because watching the factory turn away a broken engine is the whole lesson, but in a type-checked codebase a `Protocol` is often the lighter option.

In this section, we flipped the dependency so that the car and the engines both depend on a contract, and moved the failure from the grid to the factory. In the next section, we'll find out that a contract made only of method names is just half a contract.

---

## L: Liskov Substitution, or how a hybrid quietly broke everyone's code

> If S is a subtype of T, then objects of type T may be replaced with objects of type S without altering any of the desirable properties of the program.

In plain English: if your code works with a class, it should keep working when you hand it a subclass. No surprises, and no "well, *technically* it's still a car". Barbara Liskov and Jeannette Wing break that promise down into three rules:

1. **The signature rule:** a subtype implements every method with compatible argument and return types, and raises no new exceptions.
2. **The properties rule:** a subtype keeps its parent's invariants and its history.
3. **The methods rule:** a subtype can't strengthen preconditions or weaken postconditions.

Here's the catch: Python checks very little of this. An ABC checks that the methods exist, a type checker checks their signatures, and the rest is on you. Let's find out what "on you" costs!

By the late 1980s our car has telemetry, and after The Turbo Incident the team gave the car an interface too. This time the docstrings aren't decoration; they're promises, including an invariant and a promise about the history of the logs:

{{gist:L1}}

The 1980s telemetry car keeps every one of them. Note that `disable_telemetry` stops the engine first, so the invariant holds whatever order things happen in:

{{gist:L2}}

And the driver is written against that contract. It handles `TelemetryNotEnabledError` because the interface says that error can happen:

{{gist:L3}}

**2014.** The hybrid era arrives: a 1.6-litre turbo, a battery, and an energy recovery system whose MGU-H turns exhaust heat into electricity you can deploy as a boost. A hybrid is basically a telemetry car with extra hardware, so it subclasses `F1CarWithTelemetry_v1`. It was also ported at 11pm the night before testing:

{{gist:L4}}

Every change comes with a perfectly reasonable comment, and every one of them breaks the contract. **Let's hand the hybrid to the same `Driver_v2` and inspect the wreckage, one rule at a time.**

### 1. Signature rule: no surprise exceptions

Part of the signature rule does have tooling behind it. An ABC catches a *missing* method (we watched one turn away an incomplete engine back in D6), and a type checker catches an override with the wrong arguments. Nothing catches a brand-new exception:

{{gist:L5}}

The hybrid fires its boost on every push, and its battery left the garage flat. `NotEnoughElectricityError` is an exception the parent never raises, so a driver who handles exactly what the interface documents goes straight into the barriers.

### 2. Properties rule: keep the invariants

**Fine, let's charge the battery and try again:**

{{gist:L6}}

No crash! Also, no data. The invariant says the engine only runs while telemetry is recording, and `Driver_v2` relies on it: the driver switches telemetry on *when the car refuses to start*. The hybrid dropped that check, so the car starts happily, the engine runs unrecorded, and telemetry never gets switched on. No exception and no warning, just an empty list and a very confused pit wall.

### 3. Properties rule: keep the history

**This time, let's enable telemetry by hand.** Push once and note the first snapshot, then push nine more times:

{{gist:L7}}

The interface promised the log only grows: a snapshot, once recorded, never disappears. The hybrid still records every snapshot but only reports the last five, so the one the pit wall already looked at has vanished. Anything that counts, totals, or replays the logs is now quietly wrong, which is the worst kind of wrong.

### 4. Methods rule: don't get pickier (preconditions)

**Let's push with 8 mL of fuel:**

{{gist:L8}}

The parent takes any amount of fuel. The hybrid's injector only takes multiples of 5 mL, and the car passes that fussiness straight on to its callers. It shows up as yet another new exception, so it overlaps with the signature rule, but the cause is different: the method now demands more from whoever calls it. Code that was correct yesterday is wrong today, and nobody touched it.

### 5. Methods rule: don't promise less (postconditions)

**Let's work out the average fuel used per push:**

{{gist:L9}}

`get_current_telemetry` promised a snapshot that *always* includes `fuel_in_milliliters`. The hybrid swapped fuel for electricity to "save radio bandwidth", and the pit wall's fuel maths runs straight into a `KeyError`.

### The fix: keep the promises inside the subtype

Notice what we're *not* going to do: patch `Driver_v2` with an `except` for every new error and an `if` for every new quirk. That just spreads the hybrid's problems into every piece of code that ever touches a car. The hybrid made these promises the moment it subclassed `F1CarWithTelemetry_v1`, so the hybrid is where they get kept:

{{gist:L10}}

Let's break down what changed:

- **New exception:** a flat battery now means no boost, not a crash, and fuel is drawn before anything else can go wrong.
- **Invariant:** `start_engine` is inherited, so the telemetry check is back.
- **History:** `get_telemetry_logs` is inherited, so every log is kept.
- **Precondition:** any amount of fuel is welcome. The car draws exactly what was asked from the tank, the injector burns it in 5 mL pulses, and any leftover waits in the fuel line for the next push.
- **Postcondition:** the snapshot has everything the parent's did, *plus* the battery.

**And now the proof, with the very same driver:**

{{gist:L11}}

Same driver, same pit wall code, both cars, identical results. That's substitutability, and it's a lot less dramatic than the alternative.

In this section, we saw that Single Responsibility, Open/Closed, and Dependency Inversion shape how your code is built, while Liskov is about everyone who *uses* it. The rushed hybrid ran fine on its own; it was everyone relying on its contract who ended up in the gravel. Tools can check that a contract's methods exist and that the signatures line up, but everything else lives in docstrings and tests, and a subclass has to honour those too. In the next section, we'll see what happens when one contract tries to cover every car the team has ever built.

---

## I: Interface Segregation, or one driver and three generations of car

> Clients should not be forced to depend on methods they do not use.

**Heritage demo day.** The team takes three generations of car to a festival: a 1950s car, the 1980s telemetry car, and the 2014 hybrid. One driver, three cars, one very long afternoon.

The only car abstraction we have is `F1CarInterface`, and a 1950s car can't implement it with a straight face:

{{gist:I1}}

The interface forces four telemetry methods onto a car whose most advanced sensor is the driver's right foot, and every stub is a fib. `get_telemetry_logs` returning `[]` looks exactly like the broken invariant from the Liskov section, and `get_current_telemetry` breaks the promise to always include fuel. The car can't keep the invariant either, because its engine runs with nothing recording it. A bloated interface doesn't just add boilerplate; it makes Liskov violations unavoidable.

The driver has the opposite problem. They want the hybrid's boost for overtaking, but `F1CarInterface` has never heard of boost, so the driver has to peek under the bodywork to find out what they're driving:

{{gist:I2}}

Those `isinstance` checks name a concrete class. That's the Dependency Inversion problem from the turbo section wearing a fake moustache, with an Open/Closed violation thrown in for free: a `HybridF1Car_v3`, or next year's car, means editing the driver.

So the interface is too big *and* too small. It bundles three capabilities (starting, accelerating, and telemetry) that not every car has, and it has no way to say that a car can boost.

**Let's split it into one interface per capability, and add the missing one:**

{{gist:I3}}

Look closely at `StartableInterface`: it says a car may refuse to start with `StartRefusedError`. Telemetry cars refuse with `TelemetryNotEnabledError`, which subclasses it, so a telemetry car is still an honest `Startable`. Sneaking a surprise exception back in straight after the Liskov section would have been a bit embarrassing.

**Each car now signs up for exactly what it can do** (the class bodies are elided here; the full classes are in the repo):

{{gist:I4}}

The 1950s car can stop pretending, and the hybrid finally gets to brag that it's boostable. **Now let's write drivers for a set of capabilities:**

{{gist:I5}}

Let's break this down:

- `DriverForBasicCar` handles `StartRefusedError` because `StartableInterface` says it can happen, so even if you hand it a telemetry car, it reports the refusal instead of crashing.
- `DriverForHybridCar` calls `enable_boost()` because every car it's given promises `BoostableInterface`: no `isinstance`, no peeking.
- The drivers deliberately don't inherit from each other. A hybrid driver needs a boostable car, which is a *stronger precondition* than a basic driver has, and we all know how Liskov feels about that by now!

Something still has to match drivers to cars. That decision lives in exactly one place, and it asks about capabilities rather than concrete classes:

{{gist:I6}}

**It's demo day:**

{{gist:I7}}

In this section, we split one bloated interface into small ones, so every car can keep its promises honestly and every driver asks for exactly what it needs. There is a trade-off: a genuinely new *combination* of capabilities needs a new driver and one new branch in `DriverFactory`. That's still an edit, but a small one in a single place, checking abstractions, instead of `isinstance` checks against concrete classes sprinkled through every method of every driver.

---

## Conclusion

Thanks for reading, and hopefully, this has helped SOLID click! Five principles, one car, and each fix made the next one possible:

- **Single Responsibility** took construction out of the car, which is what let us hand the car its parts.
- **Open/Closed** let the car take any part without being edited, but "any part" was an assumption nobody checked.
- **Dependency Inversion** turned that assumption into a contract both sides depend on, and moved the failure from the grid to the factory, or to the type checker.
- **Liskov Substitution** made the contract mean something: a subtype keeps the promises, not just the method names.
- **Interface Segregation** kept the contracts small enough that every car could keep them honestly.

F1 teams don't win by predicting next season's rules; they win by building cars that can take whatever the rulebook throws at them. SOLID won't predict your next requirement either, but it can turn it into a new class instead of a lost weekend.

All the code, the tests that check every snippet in this article, and the interactive marimo notebook are on GitHub at [rawmarshmellows/modeling-f1-cars-with-SOLID-foundations](https://github.com/rawmarshmellows/modeling-f1-cars-with-SOLID-foundations). Clone it, break a contract, and see who ends up in the barriers. If you've got your own SOLID horror story (or a better F1 pun), please comment below and share!

*Thanks for reading. If you're interested in technical articles in AI, Python, and Javascript on a sporadic basis, please hit the follow button!*
