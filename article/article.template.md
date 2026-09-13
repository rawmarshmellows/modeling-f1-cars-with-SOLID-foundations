# 5 principles to survive a product manager who keeps changing the requirements

*Let SOLID help you set boundaries between your code, and your product manager*

{{image:slack/intro|Pat from Product on Slack: Hey! super small thing, can we add notifications to the app? Should be quick}}

Meet Pat. Pat is from Product. Pat is lovely, Pat remembers everyone's birthday, and Pat has never once asked for a change that turned out to be small.

If you've shipped software for more than a week, you've met a Pat. The requirements change on Monday, again on Wednesday, and one more time at 4:47pm on Friday. None of it is really Pat's fault (the customers, the board and the competitors all have opinions), but it's Pat's messages that land in your Slack.

{{image:memes/intro_iceberg|Iceberg meme: above the water, Pat says it's a small change; below the water, a new SMS vendor, an append-only audit log, AI by Friday, an enterprise demo tomorrow, and "actually, can we go back to email?"}}

**What if the next "small change" really was small?**

That's what the SOLID principles are for. This article will show how we can use them to survive a year of Pat's requirements while building a notifications service in Python:

- **S**ingle Responsibility: test an email channel without building the whole notifier
- **O**pen/Closed: pivot from email to SMS to push to Slack without editing the notifier
- **D**ependency Inversion: survive a cheaper SMS vendor whose SDK does things its own way
- **L**iskov Substitution: add AI without quietly breaking compliance
- **I**nterface Segregation: demo three pricing plans to an enterprise customer without writing one runner that knows them all

Yes, that spells SODLI. We take the principles in the order the code needs them, because Dependency Inversion hands out the interfaces that Liskov and Interface Segregation rely on. Sorry, acronym fans.

Each principle starts with a message from Pat, and after that it's code all the way down: what broke, why it broke, and how we fixed it. Hopefully, by the end of this article, SOLID will feel less like a job-interview acronym and more like a healthy set of boundaries between your code, and your product manager!

Every snippet below is a real file from the companion repo, and the test suite runs every one of them, so nothing here only works on slides. If you'd rather poke at the code than read about it, everything is self-contained, so there's no setup beyond:

```bash
git clone https://github.com/rawmarshmellows/surviving-pat-from-product-with-solid
cd surviving-pat-from-product-with-solid
uv run marimo edit notebook.py
```

That opens an interactive marimo notebook that follows this article section by section, so you can break things on purpose.

Let's open Slack.

---

## S: Single Responsibility, or why your notifier shouldn't build its own email channel

> A class should have one, and only one, reason to change.

{{image:slack/s|Pat on Slack: QA says they can't test the new email template without spinning up the entire notifier, can we fix by EOD?}}

**Here's our first notifier. Count its jobs:**

{{gist:S1}}

Two! `Notifier_v1` *sends* (connect, disconnect, send a message), and it also *builds* every part it sends with. It's the barista who insists on growing their own coffee beans. Because of that second job, the knowledge of *which* channel the team uses, which email server it talks to, and who the emails come from, all lives inside the notifier.

**Let's test the email channel:**

{{gist:S2}}

Translated from Product, "test the email template" means QA wants to check the email channel, and to do that we build an entire notifier: a template, a recipient list, and a credit balance with 1,000 credits in it. Worse, when the team moves to a new email server, the file they have to open is the notifier, even though nothing about sending has changed. That's two reasons to change in one class.

**Let's hire a channel shop, a class whose only job is building channels:**

{{gist:S3}}

The real `ChannelFactory` has one `create_…` method per channel; this excerpt shows the first. Templates, recipient lists, and credit balances get their own shops too, so the notifier can go back to doing what it's good at:

{{gist:S4}}

The factory is now the one place that knows how the team builds its channels. The notifier uses it, and so can QA's test, with no notifier anywhere in sight:

{{gist:S5}}

{{image:memes/s_drake|Reject-and-approve meme: no to emailing the whole company to test one template, yes to testing EmailChannel_v1 on its own}}

In this section, we split building from sending: the notifier sends, the factory builds, and when a channel comes out wrong, you know exactly whose door to knock on. Fixed by EOD, too! In the next section, Pat has BIG NEWS.

---

## O: Open/Closed, or how to pivot without opening up the notifier

> Software entities should be open for extension, but closed for modification.

{{image:slack/o|Pat on Slack: BIG NEWS, customers hate email, we're pivoting to SMS, that's a one-line change right? Then: update, push notifications are the future. Then: update 2, every enterprise lives in Slack}}

"That's a one-line change right??" Pat is technically correct, which is the most dangerous kind of correct. **Let's pivot to SMS:**

{{gist:O1}}

One line (plus the version bump). What could possibly go wrong? Well, that line lives inside the notifier, so "new channel" means "new notifier class". `Notifier_v3` needs testing from scratch even though its template, recipients, and credits haven't changed, and the next pivot means doing it all over again (spoiler: there are two more before 4:30pm). The only way to extend this notifier is to take a spanner to it.

**Let's stop the notifier from picking its own parts, and hand them over through the constructor instead:**

{{gist:O2}}

Now whoever assembles the notifier decides what goes into it:

{{gist:O3}}

**Let's take Pat's next two updates** and count how many times we have to edit the notifier class:

{{gist:O4}}

Zero! Three pivots, one class. `Notifier_v4` is **closed for modification** because nothing inside it changes, and **open for extension** because any channel plugs right in.

{{image:memes/o_expanding_brain|Expanding brain meme: Email, SMS, Push notifications, Slack, and at the most enlightened level, zero edits to Notifier_v4}}

In this section, we moved the choice of parts out of the notifier, so a new channel no longer means a new notifier. Well... *almost* any channel. In the next section, Finance finds a bargain. Cue the ominous music.

---

## D: Dependency Inversion, or surviving a cheaper SMS vendor

> High-level modules should not depend on low-level modules. Both should depend on abstractions.

{{image:slack/d|Friday, 4:47pm, Pat on Slack: Finance found a cheaper SMS vendor, TextBlaster! Already signed the contract, we go live Monday}}

TextBlaster's SDK does everything our old SMS gateway did, with one tiny difference that absolutely nobody mentioned on the sales call: you open a connection with `open_socket()` instead of `connect()`.

{{gist:D1}}

`Notifier_v4` takes any channel, so in it goes. **Let's kick off Monday's campaign.** `CampaignRunner_v1.start_campaign` simply calls `notifier.connect()`:

{{gist:D2}}

{{image:memes/d_this_is_fine|This is fine meme: Monday, 9:01am, a developer at a desk surrounded by flames under an AttributeError saying TextBlasterSmsChannel_v1 has no attribute connect}}

It turns out our Open/Closed win came with some small print: the notifier accepts *any* channel, but it quietly assumes every channel has a `connect()` method, and nothing checks.

The campaign is down and Pat is typing..., so somebody reaches for the quick fix and teaches the notifier about each channel:

{{gist:D3}}

It works! It also undoes everything the last section achieved. The notifier imports concrete channel classes again, needs editing for every new vendor, and silently does nothing for any channel it doesn't recognise, including the email, push, and Slack channels we were so proud of five minutes ago. The real problem is which way the dependency points: the high-level notifier depends on low-level channels.

Dependency Inversion turns that around. **Let's have the notifier team write down what it needs from a channel, so both sides depend on that abstraction instead:**

{{gist:D4}}

Let's break this down:

- Python has no `interface` keyword, so an abstract base class (ABC) does the job.
- It lives in `notifications/notifiers/`, the notifier team's package. The channels import it from there, so the low-level parts now depend on something the high-level notifier owns. That's the "inversion"!
- It also declares the `is_connected` flag every channel already keeps, so the notifier can rely on it too.
- Our own email, SMS, push, and Slack channels already had all of this, so each one signed up with an import and a one-line change.

**TextBlaster signs up too:**

{{gist:D5}}

It signed, but it still doesn't have a `connect()` method. **Let's see how that goes:**

{{gist:D6}}

This is the good kind of failure. The mistake that used to take down Monday's campaign now blows up the moment the channel is built, back in the factory, long before it gets anywhere near production. To pass inspection, the channel has to deliver what it signed up for:

{{gist:D7}}

**Finally, let's have the notifier say out loud what it depends on.** The whole change is an import and a type annotation:

{{gist:D8}}

The notifier still knows nothing about TextBlaster and the campaign runner hasn't changed, but this time we're connected:

{{gist:D9}}

`Notifier_v5` doesn't know or care which vendor is behind its channel. It names `ChannelInterface` as the thing it needs, and every channel that wants to plug in implements it. We also get two safety nets thrown in for free:

- The ABC rejects a channel that signs the contract but doesn't deliver, the moment it's built.
- A type checker such as mypy rejects a channel that never signed at all, like TextBlaster's original SDK, before the code even runs.

> **ABC or `typing.Protocol`?** A `Protocol` describes the same contract structurally, with no subclassing (the channels wouldn't even need to import it), and a type checker such as mypy or pyright enforces it before the code runs. An ABC is enforced at runtime, when the object is created (and mypy flags the D6 mistake too). We're using ABCs because watching the factory turn away a broken channel is the whole lesson, but in a type-checked codebase a `Protocol` is often the lighter option.

In this section, we flipped the dependency so that the notifier and the channels both depend on a contract, and moved the failure from production to the factory. In the next section, the board discovers AI, and we find out that a contract made only of method names is just half a contract.

---

## L: Liskov Substitution, or how AI quietly broke compliance

> If S is a subtype of T, then objects of type T may be replaced with objects of type S without altering any of the desirable properties of the program.

{{image:slack/l|Pat on Slack: The board asked about our AI strategy, can notifications be AI-powered by Friday? Just make them pop. Then on Monday: Compliance is asking why the audit log is empty, did something change?}}

In plain English: if your code works with a class, it should keep working when you hand it a subclass. No surprises, and no "well, *technically* it's still a notifier". Barbara Liskov and Jeannette Wing break that promise down into three rules:

1. **The signature rule:** a subtype implements every method with compatible argument and return types, and raises no new exceptions.
2. **The properties rule:** a subtype keeps its parent's invariants and its history.
3. **The methods rule:** a subtype can't strengthen preconditions or weaken postconditions.

Here's the catch: Python checks very little of this. An ABC checks that the methods exist, a type checker checks the signatures you've annotated, and the rest is on you. Let's find out what "on you" costs!

By now, compliance has been involved for a while, so our notifiers have an audit log and an interface of their own. This time the docstrings aren't decoration; they're promises, including an invariant (nothing is ever sent unaudited) and a promise about the history of the audit log:

{{gist:L1}}

The audited notifier keeps every one of them. Note how the invariant is kept from three sides: `connect` refuses without an audit log, `send` refuses without a connection, and `disable_audit_log` disconnects first:

{{gist:L2}}

And the campaign runner is written against that contract. It handles `AuditLogDisabledError`, `NotConnectedError`, and `NotEnoughCreditsError` because the interface says those can happen:

{{gist:L3}}

Then the board asks about AI. The AI notifier is an audited notifier with an AI channel and a token budget, so it subclasses `AuditedNotifier_v1`. It was also built between Wednesday lunch and Friday at 5pm:

{{gist:L4}}

{{image:memes/l_two_buttons|Two buttons meme: a red button labelled keep the compliance contract and another labelled ship AI by Friday, above a sweating face captioned me, Thursday night}}

Every change comes with a perfectly reasonable comment, and every one of them breaks the contract. **Let's hand the AI notifier to the same `CampaignRunner_v2` and inspect the wreckage, one rule at a time.**

### 1. Signature rule: no surprise exceptions

Part of the signature rule does have tooling behind it. An ABC catches a *missing* method (we watched one turn away TextBlaster's half-finished channel back in D6), and once the methods are annotated, a type checker catches an override with the wrong arguments. Nothing catches a brand-new exception:

{{gist:L5}}

The AI notifier rewrites every message by default, and its token budget starts empty. `OutOfTokensError` is an exception the parent never raises, so a runner that handles exactly what the interface documents falls over on the very first message of the campaign.

### 2. Properties rule: keep the invariants

**Fine, let's top up the tokens and try again:**

{{gist:L6}}

No crash! Also, no audit trail. The invariant says the notifier is never connected while the audit log is off, and `CampaignRunner_v2` relies on it: the runner switches the audit log on *when the notifier refuses to connect*. The AI notifier dropped that check, so it connects happily, `send` sees a connection and goes ahead, and the audit log never gets switched on. No exception and no warning, just an empty list and a Monday-morning message from Pat about compliance.

### 3. Properties rule: keep the history

**This time, let's enable the audit log by hand.** Send once and note the first entry, then send nine more:

{{gist:L7}}

The interface promised that the audit log is append-only: an entry, once recorded, never disappears. The AI notifier deletes all but the last five entries after every send "because storage isn't free", so the entry compliance already looked at is gone for good. Anything that counts, totals, or replays the log is now quietly wrong, which is the worst kind of wrong, and in an audit log, possibly the illegal kind.

### 4. Methods rule: don't get pickier (preconditions)

**Let's send the big sale promo:**

{{gist:L8}}

The parent sends a message of any length and bills it per 160-character segment. The AI model only rewrites one segment at a time (its interface says so), but the hurried notifier hands it the whole message and passes that fussiness straight on to its callers. It shows up as yet another new exception, so it overlaps with the signature rule, but the cause is different: the method now demands more from whoever calls it. A campaign that was correct yesterday is broken today, and nobody touched it.

### 5. Methods rule: don't promise less (postconditions)

**Let's run compliance's billing report:**

{{gist:L9}}

`get_current_audit_entry` promised an entry that *always* includes `credits_remaining`. The AI notifier swapped credits for tokens "because the board only asks about AI", and compliance's billing report runs straight into a `KeyError`.

### The fix: keep the promises inside the subtype

Notice what we're *not* going to do: patch `CampaignRunner_v2` with an `except` for every new error and an `if` for every new quirk. That just spreads the AI notifier's problems into every piece of code that ever touches a notifier. The AI notifier made these promises the moment it subclassed `AuditedNotifier_v1`, so the AI notifier is where they get kept:

{{gist:L10}}

Let's break down what changed:

- **New exception:** not enough tokens now means no rewrite, not a crash.
- **Invariant:** `connect` is inherited, so the audit check is back.
- **History:** nothing deletes audit entries any more, so every entry is kept.
- **Precondition:** a message of any length is welcome. It's split into segments first, and the model rewrites them one at a time.
- **Billing:** one credit per segment, charged up front. The model turns a segment into a segment, so rewriting can't change the bill.
- **Postcondition:** the audit entry has everything the parent's did, *plus* the token budget.

**And now the proof, with the very same runner:**

{{gist:L11}}

Same runner, same billing report, both notifiers (with the AI rewrites switched on this time), identical results. That's substitutability, and it's a lot less dramatic than a compliance incident.

In this section, we saw that Single Responsibility, Open/Closed, and Dependency Inversion shape how your code is built, while Liskov is about everyone who *uses* it. The rushed AI notifier worked fine on its own; it was everyone relying on its contract who got paged. Tools can check that a contract's methods exist and that the signatures line up, but everything else lives in docstrings and tests, and a subclass has to honour those too. In the next section, Pat books an enterprise demo for tomorrow morning.

---

## I: Interface Segregation, or three pricing plans and one very small factory

> Clients should not be forced to depend on methods they do not use.

{{image:slack/i|Pat on Slack: HUGE enterprise demo tomorrow, they want the legacy email plan, the compliance plan, and the AI plan side by side, one campaign runner for all three, easy right?}}

Three plans: the legacy email plan (it predates compliance, so no audit log), the compliance plan (audited), and the AI plan (audited, with AI rewrites). Pat wants one campaign runner for all three, by tomorrow morning.

The only notifier abstraction we have is `NotifierInterface`, and the legacy plan can't implement it with a straight face:

{{gist:I1}}

The interface forces four audit-log methods onto a plan that predates compliance, and every stub is a fib. `get_audit_log` returning `[]` looks exactly like the broken invariant from the Liskov section, and `get_current_audit_entry` breaks the promise to always include `credits_remaining`. The legacy plan can't keep the invariant either, because it connects with nothing auditing it. A bloated interface doesn't just add boilerplate; it makes Liskov violations unavoidable.

{{image:memes/i_same_picture|They're the same picture meme: compliance asks for the differences between two framed empty lists, the legacy plan's get_audit_log and get_audit_log with the audit log off; they're the same picture}}

The campaign runner has the opposite problem. For the demo, it should save AI tokens for the big announcement, but `NotifierInterface` has never heard of AI rewrites, so the runner has to peek under the hood to find out which plan it's holding:

{{gist:I2}}

Those `isinstance` checks name a concrete class. That's the Dependency Inversion problem from the TextBlaster section wearing a fake moustache, with an Open/Closed violation thrown in for free: an `AiNotifier_v3`, or whatever Pat asks for next quarter, means editing the runner.

So the interface is too big *and* too small. It bundles three capabilities (connecting, sending, and auditing) that not every plan has, and it has no way to say that a plan can do AI rewrites.

**Let's split it into one interface per capability, and add the missing one:**

{{gist:I3}}

Look closely at `ConnectableInterface`: it says a notifier may refuse to connect with `ConnectRefusedError`. Audited notifiers refuse with `AuditLogDisabledError`, which subclasses it, so an audited notifier is still an honest `Connectable`. Sneaking a surprise exception back in straight after the Liskov section would have been a bit embarrassing.

**Each plan now signs up for exactly what it can do** (the class bodies are elided here; the full classes are in the repo):

{{gist:I4}}

The legacy plan can stop pretending, and the AI plan finally gets to say out loud that it can rewrite. **Now let's write a campaign runner for each set of capabilities:**

{{gist:I5}}

Let's break this down:

- Every runner handles `ConnectRefusedError`, `NotConnectedError`, and `NotEnoughCreditsError`, because the interfaces say they can happen. Hand `BasicCampaignRunner` an audited notifier and it reports the refusal, and its sends stop instead of going out unaudited.
- `AiCampaignRunner` calls `enable_ai_rewrite()` because every notifier it's given promises `AiRewritableInterface`: no `isinstance`, no peeking.
- The runners deliberately don't inherit from each other. An AI runner needs an AI-rewritable notifier, which is a *stronger precondition* than a basic runner has, and we all know how Liskov feels about that by now!

Something still has to match runners to plans. That decision lives in exactly one place, it asks about capabilities rather than concrete classes, and it refuses anything it doesn't know how to run:

{{gist:I6}}

Pat asked for one campaign runner. Pat is getting one factory and three tiny runners, and Pat does not need to know. **It's demo day:**

{{gist:I7}}

In this section, we split one bloated interface into small ones, so every plan keeps its promises honestly and every runner asks for exactly what it needs. There is a trade-off: a genuinely new *combination* of capabilities needs a new runner and one new branch in `CampaignRunnerFactory`. That's still an edit, but a small one in a single place, checking abstractions, and until someone makes it, the factory raises a `TypeError` instead of guessing. Compare that with `isinstance` checks against concrete classes sprinkled through every method of every runner.

---

## Conclusion

The demo went great. Then, the following Monday:

{{image:slack/outro|Pat on Slack: So, customers actually kind of liked email, can we go back? You reply: sure, with a one-line diff in notifications/wiring.py swapping the Slack channel for the email channel}}

Of course. And thanks to `wiring.py`, the one file that decides which parts go into which notifier, going back to email really is a one-line change this time:

{{image:memes/outro_stonks|Stonks meme: Pat asks can we go back to email, I change one line in wiring.py, and a rising green chart says stonks}}

Thanks for reading, and hopefully, this has helped SOLID click! Five principles, one Pat, and each fix made the next one possible:

- **Single Responsibility** took construction out of the notifier, which is what let us hand the notifier its parts.
- **Open/Closed** let the notifier take any channel without being edited, but "any channel" was an assumption nobody checked.
- **Dependency Inversion** turned that assumption into a contract both sides depend on, and moved the failure from production to the factory, or to the type checker.
- **Liskov Substitution** made the contract mean something: a subtype keeps the promises, not just the method names.
- **Interface Segregation** kept the contracts small enough that every plan could keep them honestly.

Pat will never stop changing the requirements, and honestly, that's Pat's job. SOLID won't predict the next Slack message either, but it can turn it into a new class instead of a lost weekend.

All the code, the tests that check every snippet in this article, and the interactive marimo notebook are on GitHub at [rawmarshmellows/surviving-pat-from-product-with-solid](https://github.com/rawmarshmellows/surviving-pat-from-product-with-solid). Clone it, break a contract, and see who gets paged. If you've got your own Pat story (or you *are* Pat, hi!), please comment below and share!

*Thanks for reading. If you're interested in technical articles in AI, Python, and Javascript on a sporadic basis, please hit the follow button!*
