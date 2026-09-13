# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.24",
# ]
# ///

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", app_title="SOLID vs. Pat from Product")

with app.setup:
    import marimo as mo

    from notifications.billing import CreditBalanceFactory
    from notifications.billing.pricing import segments_of
    from notifications.campaigns import CampaignRunnerFactory
    from notifications.campaigns.campaign_runner_v1 import CampaignRunner_v1
    from notifications.campaigns.campaign_runner_v2 import CampaignRunner_v2
    from notifications.channels import ChannelFactory
    from notifications.notifiers.ai_notifier_v1 import AiNotifier_v1
    from notifications.notifiers.ai_notifier_v2 import AiNotifier_v2
    from notifications.notifiers.ai_notifier_v3 import AiNotifier_v3
    from notifications.notifiers.audited_notifier_v1 import AuditedNotifier_v1
    from notifications.notifiers.audited_notifier_v2 import AuditedNotifier_v2
    from notifications.notifiers.notifier_v1 import Notifier_v1
    from notifications.notifiers.notifier_v4 import Notifier_v4
    from notifications.notifiers.notifier_v5 import Notifier_v5
    from notifications.notifiers.notifier_v7 import Notifier_v7
    from notifications.recipients import RecipientListFactory
    from notifications.templates import TemplateFactory
    from notifications.wiring import build_ai_notifier, build_audited_notifier, build_legacy_notifier
    from snippets.catalog import snippet_markdown

    BIG_SALE_PROMO = "Everything must go! " * 10  # 200 characters, two SMS segments


@app.function
def show_code(snippet_id):
    """Show a snippet exactly as it appears in the article and in its gist."""
    return mo.md(snippet_markdown(snippet_id))


@app.function
def pat(name):
    """One of Pat's Slack messages."""
    return mo.image(src=str(mo.notebook_dir() / "images" / "slack" / f"{name}.png"), width=640, rounded=True)


@app.function
def meme(name, alt):
    return mo.image(src=str(mo.notebook_dir() / "images" / "memes" / f"{name}.png"), alt=alt, width=460, rounded=True)


@app.function
def outcome(action):
    """Run `action` and show the result, or the exception it raised, without halting the notebook."""
    try:
        result = action()
    except Exception as error:
        return mo.callout(mo.md(f"**{type(error).__name__}**\n\n```text\n{error}\n```"), kind="danger")
    return mo.callout(mo.md("No error raised" if result is None else str(result)), kind="success")


@app.function
def average_credits_per_send(audit_log):
    """Compliance's billing report, written against the promise in NotifierInterface.get_current_audit_entry."""
    credits = [entry["credits_remaining"] for entry in audit_log]
    return (credits[0] - credits[-1]) / (len(credits) - 1)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # 5 principles to survive a product manager who keeps changing the requirements

    Meet Pat. Pat is from Product, Pat is lovely, and Pat has never once asked for a change that turned out
    to be small.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.vstack([pat("intro"), meme("intro_iceberg", "Iceberg: it's a small change")])
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    **What if the next "small change" really was small?**

    That's what SOLID is for. This notebook follows the article section by section, building a notifications
    service that survives a year of Pat's requirements. We take the principles in the order the code needs
    them, **S → O → D → L → I** (yes, SODLI), because Dependency Inversion hands out the interfaces that Liskov
    and Interface Segregation rely on.

    - Read-only code blocks are the exact snippets from the article (and its gists).
    - Code cells are live, so edit them, break a contract, and see who gets paged!
    - Deliberate crashes show up as red callouts, so the rest of the notebook keeps running.

    Let's open Slack.

    ---
    ## S: Single Responsibility, or why your notifier shouldn't build its own email channel

    > A class should have one, and only one, reason to change.
    """)
    return


@app.cell(hide_code=True)
def _():
    pat("s")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    **Here's our first notifier. Count its jobs:**
    """)
    return


@app.cell(hide_code=True)
def _():
    show_code("S1")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Two! It *sends*, and it *builds* every part it sends with, so the knowledge of which channel the team
    uses lives inside the notifier. **Let's test the email channel:**
    """)
    return


@app.cell
def _():
    def _test_email_channel_connects():
        notifier = Notifier_v1()  # only the notifier knows which channel to build, so we build all of it
        notifier.connect()
        assert notifier.channel.is_connected


    _test_email_channel_connects()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    **Let's hire a channel shop, a class whose only job is building channels**, and let the notifier ask
    factories for its parts:
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


@app.cell
def _():
    def _test_email_channel_connects():
        channel = ChannelFactory.create_email_channel_v1()  # built exactly the way the notifier builds it
        channel.connect()
        assert channel.is_connected


    _test_email_channel_connects()
    return


@app.cell(hide_code=True)
def _():
    meme("s_drake", "Reject emailing the whole company, approve testing EmailChannel_v1 on its own")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    In this section, we split building from sending: the notifier sends, the factory builds. Fixed by EOD!
    In the next section, Pat has BIG NEWS.

    ---
    ## O: Open/Closed, or how to pivot without opening up the notifier

    > Software entities should be open for extension, but closed for modification.
    """)
    return


@app.cell(hide_code=True)
def _():
    pat("o")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    "That's a one-line change right??" Pat is technically correct, the most dangerous kind of correct.
    **Let's pivot to SMS:**
    """)
    return


@app.cell(hide_code=True)
def _():
    show_code("O1")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    One line, but it lives inside the notifier, so every pivot means a new notifier class. **Let's hand the
    notifier its parts through the constructor instead:**
    """)
    return


@app.cell(hide_code=True)
def _():
    show_code("O2")
    return


@app.cell
def _():
    sms_notifier = Notifier_v4(
        channel=ChannelFactory.create_sms_channel_v1(),
        template=TemplateFactory.create_plain_text_template_v1(),
        recipients=RecipientListFactory.create_recipient_list_v1(),
        credit_balance=CreditBalanceFactory.create_credit_balance_v1(),
    )
    sms_notifier.connect()
    sms_notifier.send("Your order has shipped! 📦")
    sms_notifier.credit_balance.credits.amount
    return (sms_notifier,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    **Let's take Pat's next two updates**, and count the edits to `Notifier_v4`:
    """)
    return


@app.cell
def _(sms_notifier):
    # Pivot #2: "push notifications are the future"
    push_notifier = Notifier_v4(
        channel=ChannelFactory.create_push_channel_v1(),
        template=TemplateFactory.create_rich_card_template_v1(),
        recipients=RecipientListFactory.create_recipient_list_v1(),
        credit_balance=CreditBalanceFactory.create_credit_balance_v1(),
    )

    # Pivot #3: "every enterprise lives in Slack"
    slack_notifier = Notifier_v4(
        channel=ChannelFactory.create_slack_channel_v1(),
        template=TemplateFactory.create_rich_card_template_v1(),
        recipients=RecipientListFactory.create_recipient_list_v1(),
        credit_balance=CreditBalanceFactory.create_credit_balance_v1(),
    )

    # Three pivots, one class, zero edits to Notifier_v4
    [type(_notifier.channel).__name__ for _notifier in (sms_notifier, push_notifier, slack_notifier)]
    return


@app.cell(hide_code=True)
def _():
    meme("o_expanding_brain", "Email, SMS, push, Slack, zero edits to Notifier_v4")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### 🛠️ Pivot it yourself

    Pick any channel and template. `Notifier_v4` takes them all without an edit... *almost*. Try
    **TextBlaster (v1)** before reading the next section.
    """)
    return


@app.cell
def _():
    channel_picker = mo.ui.dropdown(
        options={
            "📧 Email": ChannelFactory.create_email_channel_v1,
            "💬 SMS": ChannelFactory.create_sms_channel_v1,
            "🔔 Push": ChannelFactory.create_push_channel_v1,
            "#️⃣ Slack": ChannelFactory.create_slack_channel_v1,
            "💸 TextBlaster (v1)": ChannelFactory.create_textblaster_sms_channel_v1,
        },
        value="💬 SMS",
        label="Channel",
    )
    template_picker = mo.ui.dropdown(
        options={
            "Plain text": TemplateFactory.create_plain_text_template_v1,
            "HTML": TemplateFactory.create_html_template_v1,
            "Rich card": TemplateFactory.create_rich_card_template_v1,
        },
        value="Plain text",
        label="Template",
    )
    mo.hstack([channel_picker, template_picker], justify="start")
    return channel_picker, template_picker


@app.cell
def _(channel_picker, template_picker):
    _notifier = Notifier_v4(
        channel=channel_picker.value(),
        template=template_picker.value(),
        recipients=RecipientListFactory.create_recipient_list_v1(),
        credit_balance=CreditBalanceFactory.create_credit_balance_v1(),
    )


    def _connect_and_send():
        with mo.capture_stdout() as output:
            CampaignRunner_v1().start_campaign(_notifier)
            _notifier.send("Your order has shipped! 📦")
        return f"`Notifier_v4` sent it\n\n```text\n{output.getvalue()}```"


    outcome(_connect_and_send)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    In this section, we moved the choice of parts out of the notifier. Well... *almost* any part.
    Cue the ominous music.

    ---
    ## D: Dependency Inversion, or surviving a cheaper SMS vendor

    > High-level modules should not depend on low-level modules. Both should depend on abstractions.
    """)
    return


@app.cell(hide_code=True)
def _():
    pat("d")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    TextBlaster's SDK has one tiny difference nobody mentioned on the sales call: `open_socket()` instead of `connect()`.
    """)
    return


@app.cell(hide_code=True)
def _():
    show_code("D1")
    return


@app.cell
def _():
    textblaster_notifier_v4 = Notifier_v4(
        channel=ChannelFactory.create_textblaster_sms_channel_v1(),
        template=TemplateFactory.create_plain_text_template_v1(),
        recipients=RecipientListFactory.create_recipient_list_v1(),
        credit_balance=CreditBalanceFactory.create_credit_balance_v1(),
    )
    outcome(lambda: CampaignRunner_v1().start_campaign(textblaster_notifier_v4))
    return


@app.cell(hide_code=True)
def _():
    meme("d_this_is_fine", "Monday 9:01am, this is fine")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    The notifier quietly assumed every channel has `connect()`. The tempting Monday-morning patch teaches the
    notifier about each channel, undoes Open/Closed, and silently skips any channel it doesn't recognise:
    """)
    return


@app.cell(hide_code=True)
def _():
    show_code("D3")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    **Let's have the notifier team write down what it needs from a channel**, in its own package
    (`notifications/notifiers/`), so both sides depend on that abstraction. Our own channels already fit;
    TextBlaster signs up too:
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
    It signed, but still has no `connect()`. The mistake that took down Monday's campaign now fails in the factory:
    """)
    return


@app.cell
def _():
    outcome(ChannelFactory.create_textblaster_sms_channel_v2)
    return


@app.cell(hide_code=True)
def _():
    show_code("D7")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    **Finally, let's have the notifier say out loud what it depends on**, with an import and a type annotation
    that also lets mypy reject a channel that never signed the contract:
    """)
    return


@app.cell(hide_code=True)
def _():
    show_code("D8")
    return


@app.cell
def _():
    textblaster_notifier_v5 = Notifier_v5(
        channel=ChannelFactory.create_textblaster_sms_channel_v3(),
        template=TemplateFactory.create_plain_text_template_v1(),
        recipients=RecipientListFactory.create_recipient_list_v1(),
        credit_balance=CreditBalanceFactory.create_credit_balance_v1(),
    )
    CampaignRunner_v1().start_campaign(textblaster_notifier_v5)  # the same runner, a notifier that's never heard of TextBlaster
    textblaster_notifier_v5.channel.is_connected
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    In this section, we flipped the dependency so the notifier and the channels both depend on a contract.
    The ABC turns away a channel that signs but doesn't deliver, and a type checker rejects one that never signed.

    /// admonition | ABC or `typing.Protocol`?
    A `Protocol` describes the same contract structurally, with no subclassing, and a type checker enforces it
    before the code runs. An ABC is enforced at runtime, when the object is created. We use ABCs because watching
    the factory turn away a broken channel is the lesson.
    ///

    ---
    ## L: Liskov Substitution, or how AI quietly broke compliance

    > If S is a subtype of T, then objects of type T may be replaced with objects of type S
    > without altering any of the desirable properties of the program.
    """)
    return


@app.cell(hide_code=True)
def _():
    pat("l")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    In plain English: hand your code a subclass, and nothing should break. Liskov and Wing's three rules:

    1. **Signature rule:** implement every method with compatible types, and raise no new exceptions.
    2. **Properties rule:** keep the parent's invariants and history.
    3. **Methods rule:** don't strengthen preconditions or weaken postconditions.

    Python checks very little of this: an ABC checks that methods exist, a type checker checks annotated signatures, and
    the rest is on you. Our notifiers have an audit log now, and an interface whose docstrings make promises:
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
    Then the board asks about AI, and the AI notifier gets built between Wednesday lunch and Friday at 5pm:
    """)
    return


@app.cell(hide_code=True)
def _():
    show_code("L4")
    return


@app.cell(hide_code=True)
def _():
    meme("l_two_buttons", "Keep the compliance contract, or ship AI by Friday")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### 1. Signature rule: no surprise exceptions

    The token budget starts empty, and the AI notifier rewrites every message by default:
    """)
    return


@app.cell
def _():
    def _first_campaign_message():
        ai_notifier = build_ai_notifier(AiNotifier_v1)  # the token budget starts empty
        runner = CampaignRunner_v2()
        runner.start_campaign(ai_notifier)
        runner.send_message(ai_notifier, "Your order has shipped! 📦")


    outcome(_first_campaign_message)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### 2. Properties rule: keep the invariants

    **Fine, let's top up the tokens.** No crash, but the notifier never refuses to connect, so the runner
    never enables the audit log:
    """)
    return


@app.cell
def _():
    _ai_notifier = build_ai_notifier(AiNotifier_v1, tokens=4_000)
    _runner = CampaignRunner_v2()
    _runner.start_campaign(_ai_notifier)  # no AuditLogDisabledError, so the runner never enables the audit log
    _runner.send_message(_ai_notifier, "Your order has shipped! 📦")
    {
        "connected": _ai_notifier.channel.is_connected,
        "audit log enabled": _ai_notifier.audit_log.is_enabled,
        "audit log": _ai_notifier.get_audit_log(),
    }
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### 3. Properties rule: keep the history

    The audit log is append-only. **Let's enable it by hand**, send once and note the first entry, then send nine more:
    """)
    return


@app.cell
def _():
    _ai_notifier = build_ai_notifier(AiNotifier_v1, tokens=4_000)
    _runner = CampaignRunner_v2()
    _runner.start_campaign(_ai_notifier)
    _ai_notifier.enable_audit_log()  # enable it by hand this time
    _runner.send_message(_ai_notifier, "Your order has shipped! 📦")
    _first_entry = _ai_notifier.get_audit_log()[0]
    for _ in range(9):
        _runner.send_message(_ai_notifier, "Your order has shipped! 📦")

    {
        "first entry still in the audit log": _first_entry in _ai_notifier.get_audit_log(),
        "entries reported": len(_ai_notifier.get_audit_log()),
    }
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### 4. Methods rule: don't get pickier (preconditions)

    The parent sends a message of any length. Slide the length past 160 characters and compare the Friday
    AI notifier with the fixed one (`AiNotifier_v2`, shown further down):
    """)
    return


@app.cell
def _():
    message_length = mo.ui.slider(start=10, stop=400, step=10, value=200, label="Message length (characters)", show_value=True)
    message_length
    return (message_length,)


@app.cell
def _(message_length):
    def _send(notifier_class):
        notifier = build_ai_notifier(notifier_class, tokens=4_000)
        notifier.enable_audit_log()
        CampaignRunner_v2().start_campaign(notifier)
        message = ("Everything must go! " * 20)[: message_length.value]
        credits_before = notifier.credit_balance.credits.amount
        notifier.send(message)
        charged = credits_before - notifier.credit_balance.credits.amount
        return f"Sent {len(message)} characters in {len(segments_of(message))} segment(s) for {charged} credit(s)"


    mo.hstack(
        [
            mo.vstack([mo.md("**`AiNotifier_v1`**"), outcome(lambda: _send(AiNotifier_v1))]),
            mo.vstack([mo.md("**`AiNotifier_v2`**"), outcome(lambda: _send(AiNotifier_v2))]),
        ],
        widths="equal",
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### 5. Methods rule: don't promise less (postconditions)

    Compliance's billing report (`average_credits_per_send`, defined at the top of this notebook) relies on
    every audit entry including `credits_remaining`:
    """)
    return


@app.cell
def _():
    _ai_notifier = build_ai_notifier(AiNotifier_v1, tokens=4_000)
    _ai_notifier.enable_audit_log()
    _runner = CampaignRunner_v2()
    _runner.start_campaign(_ai_notifier)
    for _ in range(10):
        _runner.send_message(_ai_notifier, "Your order has shipped! 📦")

    outcome(lambda: average_credits_per_send(_ai_notifier.get_audit_log()))
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### The fix: keep the promises inside the subtype

    Don't patch every caller. The AI notifier made these promises when it subclassed `AuditedNotifier_v1`,
    so the AI notifier keeps them:
    """)
    return


@app.cell(hide_code=True)
def _():
    show_code("L10")
    return


@app.cell
def _():
    _notifiers = [
        build_audited_notifier(AuditedNotifier_v1),
        build_ai_notifier(AiNotifier_v2, tokens=4_000),  # AI rewrites on this time
    ]
    _runner = CampaignRunner_v2()  # not a single line of the runner has changed
    for _notifier in _notifiers:
        _runner.start_campaign(_notifier)
        for _ in range(10):
            _runner.send_message(_notifier, BIG_SALE_PROMO)

    {
        "audit entries": [len(_notifier.get_audit_log()) for _notifier in _notifiers],
        "average credits per send": [average_credits_per_send(_notifier.get_audit_log()) for _notifier in _notifiers],
    }
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    In this section, the rushed AI notifier worked fine on its own; it was everyone relying on its contract who
    got paged. Tools can check that methods exist and signatures line up, but everything else lives in docstrings
    and tests, and a subclass has to honour those too.

    ---
    ## I: Interface Segregation, or three pricing plans and one very small factory

    > Clients should not be forced to depend on methods they do not use.
    """)
    return


@app.cell(hide_code=True)
def _():
    pat("i")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    The legacy email plan predates compliance, so it can't implement `NotifierInterface` with a straight face:
    """)
    return


@app.cell(hide_code=True)
def _():
    show_code("I1")
    return


@app.cell(hide_code=True)
def _():
    meme("i_same_picture", "They're the same picture: two empty audit logs")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    And a runner that wants to save AI tokens for the big announcement has to check concrete classes:
    """)
    return


@app.cell(hide_code=True)
def _():
    show_code("I2")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    The interface is too big (three capabilities not every plan has) and too small (no way to say a plan can do
    AI rewrites). **Let's split it into one interface per capability, and add the missing one.**
    `ConnectableInterface` documents `ConnectRefusedError`, and `AuditLogDisabledError` subclasses it, so audited
    notifiers stay honest `Connectable`s:
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
    Pat asked for one campaign runner. Pat is getting one factory and three tiny runners.
    **Let's write a runner for each set of capabilities**, and let a factory pick one by asking about interfaces:
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
    _demo_plans = [
        build_legacy_notifier(Notifier_v7),
        build_audited_notifier(AuditedNotifier_v2),
        build_ai_notifier(AiNotifier_v3, tokens=4_000),
    ]
    for _notifier in _demo_plans:
        _runner = CampaignRunnerFactory.create_runner_for(_notifier)
        _runner.start_campaign(_notifier)
        _runner.send_message(_notifier, "Your order has shipped! 📦")
        _runner.send_big_announcement(_notifier, "🎉 We're live in 40 countries!")

    [type(CampaignRunnerFactory.create_runner_for(_notifier)).__name__ for _notifier in _demo_plans]
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### 🤝 Run the demo yourself

    Pick a plan, and `CampaignRunnerFactory` picks the runner. The console shows what happened.
    """)
    return


@app.cell
def _():
    plan_picker = mo.ui.dropdown(
        options={
            "Legacy email plan · Notifier_v7": lambda: build_legacy_notifier(Notifier_v7),
            "Compliance plan · AuditedNotifier_v2": lambda: build_audited_notifier(AuditedNotifier_v2),
            "AI plan · AiNotifier_v3": lambda: build_ai_notifier(AiNotifier_v3, tokens=4_000),
        },
        value="AI plan · AiNotifier_v3",
        label="Plan",
    )
    plan_picker
    return (plan_picker,)


@app.cell
def _(plan_picker):
    _notifier = plan_picker.value()
    _runner = CampaignRunnerFactory.create_runner_for(_notifier)
    with mo.capture_stdout() as _console:
        _runner.start_campaign(_notifier)
        _runner.send_message(_notifier, "Your order has shipped! 📦")
        _runner.send_big_announcement(_notifier, "🎉 We're live in 40 countries!")

    mo.vstack(
        [
            mo.md(f"`CampaignRunnerFactory` picked **`{type(_runner).__name__}`**"),
            mo.plain_text(_console.getvalue()),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    In this section, we split one bloated interface into small ones, so every plan keeps its promises honestly.
    The trade-off: a genuinely new *combination* of capabilities still needs a new runner and one branch in
    `CampaignRunnerFactory`, but that's a small edit in one place, against abstractions.

    ---
    ## Conclusion

    The demo went great. Then, the following Monday:
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.vstack([pat("outro"), meme("outro_stonks", "Stonks: one line in wiring.py")])
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Thanks for playing along, and hopefully, SOLID has clicked! Each fix made the next one possible:

    - **Single Responsibility** took construction out of the notifier, which let us hand the notifier its parts.
    - **Open/Closed** let the notifier take any channel without being edited, but "any channel" was an unchecked assumption.
    - **Dependency Inversion** turned the assumption into a contract, and moved the failure from production to the factory, or the type checker.
    - **Liskov Substitution** made the contract mean something: subtypes keep the promises, not just the method names.
    - **Interface Segregation** kept contracts small enough for every plan to keep honestly.

    Pat will never stop changing the requirements, and honestly, that's Pat's job. Now go break a contract and
    see who gets paged!
    """)
    return


if __name__ == "__main__":
    app.run()
