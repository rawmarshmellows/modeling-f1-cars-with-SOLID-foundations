# SOLID vs. Pat from Product: rewrite plan (draft v1)

> Replaces the F1 outline (git history still has it). Nothing in the code has changed yet. This is the plan to agree on first.

**Locked decisions**
- Product: a startup's notifications service. The code *is* the product, so there's no metaphor layer.
- Antagonist: **Pat from Product** (fictional). Pat sends one Slack message per section, taking the place of the one F1 moment per letter.
- Order stays S → O → D → L → I, in one article, in Kevin's Medium voice.
- Memes, made two ways:
  - Original Slack-style screenshots of Pat's messages, rendered in the repo.
  - Classic-template memes: Claude writes the captions, Kevin makes them on imgflip.
- Rename the GitHub repo and the Python package.
- All 36 gists get updated in place, so their URLs don't change.

---

## 1. Names

| Thing | Now | Proposed |
|---|---|---|
| Article title | 5 principles to stop your code from spinning out every time the rules change | **5 principles to survive a product manager who keeps changing the requirements** |
| Subtitle | Let SOLID help you build a Python F1 car… | **Let SOLID help you set boundaries between your code, and your product manager** |
| GitHub repo | `modeling-f1-cars-with-SOLID-foundations` | **`surviving-pat-from-product-with-solid`** (alternatives: `solid-vs-changing-requirements`, `pat-changed-the-requirements-again`) |
| Python package | `app/` | **`notifications/`** |
| Gist descriptions | `SOLID F1 · S1 · …` | `SOLID vs Pat · S1 · …` |
| Notebook title | F1 | same as the article title |

## 2. File renames

```
app/                                  →  notifications/
├── garage.py                         →  wiring.py                       (composition root)
├── f1_cars/                          →  notifiers/
│   ├── f1_car_v1.py … v3.py          →  notifier_v1.py … v3.py          (S, O)
│   ├── f1_car_v4.py                  →  notifier_v4.py                  (O: constructor injection)
│   ├── f1_car_v4_patched.py          →  notifier_v4_patched.py          (D: the type switch)
│   ├── engine_interface.py           →  channel_interface.py            (D: owned by the notifier team)
│   ├── hybrid_engine_interface.py    →  ai_channel_interface.py
│   ├── f1_car_v5.py                  →  notifier_v5.py                  (D: channel: ChannelInterface)
│   ├── interface.py                  →  notifier_interface.py           (L: the contract)
│   ├── f1_car_with_telemetry_v1.py   →  audited_notifier_v1.py          (L: keeps every promise)
│   ├── hybrid_f1_car_v1.py / v2.py   →  ai_notifier_v1.py / v2.py       (L: hurried / fixed)
│   ├── f1_car_v6.py                  →  notifier_v6.py                  (I: legacy plan faking an audit log)
│   ├── segregated_interfaces.py      →  segregated_interfaces.py
│   ├── f1_car_v7.py                  →  notifier_v7.py                  (I: legacy plan, split interfaces)
│   ├── f1_car_with_telemetry_v2.py   →  audited_notifier_v2.py
│   ├── hybrid_f1_car_v3.py           →  ai_notifier_v3.py
│   └── exceptions.py                 →  exceptions.py                   (ConnectRefusedError)
├── engine/                           →  channels/
│   ├── engine_1950s_1_5L_supercharged_v1.py              →  email_channel_v1.py      (S)
│   ├── engine_1950s_2_5L_naturally_aspirated_v1.py       →  sms_channel_v1.py        (O: "pivot to SMS")
│   ├── engine_1960s_1_5L_naturally_aspirated_mid_rear_v1 →  push_channel_v1.py       (O: pivot #2)
│   ├── engine_1970s_1_5L_renault_rs01_v1.py              →  slack_channel_v1.py      (O: pivot #3)
│   ├── engine_1980s_1_5L_turbocharged_v1/v2/v3.py        →  textblaster_sms_channel_v1/v2/v3.py  (D)
│   ├── engine_2010s_1_6L_hybrid_turbocharged_v1.py       →  ai_sms_channel_v1.py     (L, I)
│   ├── exceptions.py                 →  exceptions.py                   (MessageTooLongError)
│   └── factory.py                    →  factory.py                      (ChannelFactory)
├── drivers/                          →  campaigns/                      (the code that USES a notifier)
│   ├── driver_v1.py / v2.py / v3.py  →  campaign_runner_v1.py / v2.py / v3.py
│   ├── drivers_by_role.py            →  campaign_runners_by_role.py
│   └── factory.py                    →  factory.py                      (CampaignRunnerFactory)
├── fuel_tank/                        →  billing/                        (Credits, CreditBalance_v1, NotEnoughCreditsError)
├── telemetry_system/                 →  audit_log/                      (AuditLog_v1, AuditLogDisabledError)
├── battery/                          →  ai/                             (Tokens, TokenBudget_v1, OutOfTokensError)
├── chassis/                          →  templates/                      (PlainText, Html, RichCard)
├── wheels/                           →  recipients/                     (RecipientList_v1)
└── energy_recovery_system/           →  deleted
images/Alfa-Romeo-159-(1951).jpg      →  deleted; replaced by images/slack/*.png and images/memes/*.png
```

## 3. Methods and the contract

| F1 | Notifications |
|---|---|
| `start_engine()` / `stop_engine()` | `connect()` / `disconnect()` |
| `push_accelerator(fuel_amount_in_milliliters)` | `send(message)` |
| engine `inject_fuel(fuel)` (+ `inject_air`) | channel `deliver(message)` (`inject_air` dropped, so less noise in every gist) |
| fuel tank, mL of fuel | credit balance: **1 credit per 160-character SMS segment** (real SMS pricing) |
| telemetry `enable/disable/get_current/get_logs` | `enable_audit_log()`, `disable_audit_log()`, `get_current_audit_entry()`, `get_audit_log()` |
| `enable_boost()` / `disable_boost()` | `enable_ai_rewrite()` / `disable_ai_rewrite()`, a.k.a. "✨ make it pop mode" |
| battery kJ, 120 kJ per boost | AI token budget, 120 tokens per rewrite |
| driver `start_car` / `accelerate_car` / `overtake` | runner `start_campaign` / `send_message` / `send_big_announcement` |

**`NotifierInterface` promises** (the Liskov section):
- **Invariant:** the notifier is never connected while the audit log is off (compliance!). `connect()` raises `AuditLogDisabledError`, and `disable_audit_log()` disconnects first.
- **`send(message)`:** accepts a message of any length and charges exactly one credit per 160-character segment. It raises `NotEnoughCreditsError`, and nothing else.
- **`get_current_audit_entry()`:** always includes `"credits_remaining"`.
- **`get_audit_log()`:** every entry since the log was enabled, oldest first. It's append-only: an entry, once recorded, never disappears.

**`AiNotifier_v1`, "shipped by Friday"** breaks each promise:

| Rule | What it does | Its "reasonable" comment |
|---|---|---|
| New exception | rewrites every message with AI, so an empty token budget raises `OutOfTokensError` | "AI on by default, that's the whole point" |
| Invariant | `connect()` skips the audit check | "the AI logs everything anyway" |
| History | `get_audit_log()` returns only the last 5 entries | "to save storage costs" |
| Precondition | the AI channel only delivers one segment, so anything over 160 characters raises `MessageTooLongError` | "nobody reads past 160 characters" |
| Postcondition | the audit entry swaps `credits_remaining` for `tokens_remaining` | "the board only asks about AI" |

**`AiNotifier_v2`, the fixed one:**
- It skips the rewrite when tokens run out.
- It splits long messages into segments.
- It reports credits *and* tokens.
- It inherits `connect()` and `get_audit_log()`.

**Interface Segregation:** the split interfaces are `Connectable`, `Sendable`, `Auditable` and `AiRewritable`. The three plans are the legacy email plan (`Notifier_v7`), the compliance plan (`AuditedNotifier_v2`) and the AI plan (`AiNotifier_v3`). The runners are `BasicCampaignRunner`, `AuditedCampaignRunner`, `AiCampaignRunner` and `CampaignRunnerFactory`.

## 4. Pat's Slack script (one message per section)

| Where | Pat says |
|---|---|
| Intro | "Hey! 👋 super small thing, can we add notifications to the app? Should be quick 🙏" |
| S | "QA says they can't test the new email template without spinning up the *entire* notifier 😅 can we fix by EOD?" |
| O | "BIG NEWS 🚀 customers hate email. We're pivoting to SMS! That's a one-line change right??" |
| O (the fast-forward) | "update: push notifications are the future" · "update 2: every enterprise lives in Slack 🤯" |
| D (Friday, 4:47pm) | "Finance found a cheaper SMS vendor 🎉 TextBlaster! Already signed the contract, we go live Monday 🙃" |
| L | "The board asked about our AI strategy 👀 can notifications be AI-powered by Friday? Just make them ✨pop✨" |
| L (the fallout) | "Compliance is asking why the audit log is empty 😬 did something change??" |
| I | "HUGE enterprise demo tomorrow 🤝 they want the legacy email plan, the compliance plan and the AI plan side by side. One campaign runner for all three, easy right?" |
| Outro | "So… customers actually kind of liked email 😅 can we go back?" |

## 5. Memes

**Original: Slack-style screenshots** (rendered in the repo from HTML with headless Chrome)
- One PNG per Pat message above, in `images/slack/`.
- Pat is a generic initials avatar, and the look is a generic chat UI, with no Slack logo.

**Classic templates:** Claude writes the captions, Kevin makes them on imgflip and saves them as `images/memes/<name>.png`.

| File | Where | Template | Captions |
|---|---|---|---|
| `intro_iceberg.png` | Intro | Iceberg | Tip: "Pat: it's a small change". Below the water: "new SMS vendor", "compliance audit log", "AI by Friday", "enterprise demo tomorrow" |
| `s_drake.png` | S | Drake | 🙅 "Emailing the whole company to test one template" / 👍 "Testing `EmailChannel_v1` on its own" |
| `o_expanding_brain.png` | O | Expanding brain | "Email" → "SMS" → "Push notifications" → "Zero edits to `Notifier_v4`" |
| `d_this_is_fine.png` | D | This is fine | "Monday, 9:01am" / "AttributeError: 'TextBlasterSmsChannel_v1' object has no attribute 'connect'" |
| `l_two_buttons.png` | L | Two buttons | "Keep the compliance contract" / "Ship AI by Friday" |
| `i_same_picture.png` | I | They're the same picture | "`get_audit_log()` on the legacy plan" / "`get_audit_log()` with the audit log switched off" / "`[]`" |
| `outro_stonks.png` | Outro | Stonks | "Pat: can we go back to email?" / "changes one line in `wiring.py`" |

Until Kevin's PNGs exist, the article and notebook show a placeholder card with the caption text, and a test lists which memes are still missing.

## 6. What stays the same
- The five lessons and their order, and every fix from the technical review, just translated (e.g. `engine: EngineInterface` becomes `channel: ChannelInterface`, and the mypy test follows).
- The test harness, the manifest, the publish and render scripts, the marimo notebook structure, and the three interactive pieces:
  - "Build your own notifier" (channel × template)
  - a message-length slider (the precondition)
  - a plan picker (the enterprise demo)
- The same 36 gist URLs, with content and filenames updated in place.

---

## As built (2026-09-13)

Two independent technical reviews tightened the plan without changing the story:
- **Send requires a connection:** `send` refuses without one (`NotConnectedError`), so "nothing is ever sent unaudited" is true of the parent. `connect` needs the audit log, and `disable_audit_log` disconnects first.
- **The 160-character limit** belongs to the AI model (`AiChannelInterface.rewrite_with_ai` rewrites one segment). The hurried `AiNotifier_v1` hands it the whole message; `AiNotifier_v2` rewrites segment by segment, so billing can't change.
- **The history violation is real:** `AiNotifier_v1` deletes all but the last five audit entries.
- **Interface Segregation:**
  - Every runner handles the documented exceptions.
  - `CampaignRunnerFactory` raises `TypeError` for combinations it can't serve.
  - "One campaign runner" became Pat's punchline: one factory, three tiny runners.
- **Configuration and wording:**
  - `EmailChannel_v1` takes real configuration (`server`, `sender`), so building a channel involves actual knowledge.
  - The type-checker claims are qualified: mypy checks *annotated* signatures.
