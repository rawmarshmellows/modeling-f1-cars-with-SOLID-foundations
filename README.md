# Surviving Pat from Product with SOLID

SOLID principles in Python, told through a product manager who keeps changing the requirements for a notifications service.
This is the companion repo for the article **5 principles to survive a product manager who keeps changing the requirements**.

| Principle             | Pat says                                                  | What breaks, and what fixes it |
|-----------------------|-----------------------------------------------------------|--------------------------------|
| Single Responsibility | "QA can't test the email template without the whole notifier" | The notifier builds its own channel, until a factory builds it |
| Open/Closed           | "We're pivoting to SMS! (then push, then Slack)"          | Every pivot means editing the notifier, until its parts are injected |
| Dependency Inversion  | "Finance found a cheaper SMS vendor, already signed 🙃"    | A channel that connects differently takes down Monday's campaign, until both sides depend on `ChannelInterface` |
| Liskov Substitution   | "Can notifications be AI-powered by Friday?"              | A rushed AI subclass breaks every compliance promise, until it keeps the parent's contract |
| Interface Segregation | "Enterprise demo tomorrow: three plans, one runner"       | One fat interface forces the legacy plan to fake an audit log, until it's split per capability |

## Run it

You need [uv](https://docs.astral.sh/uv/getting-started/installation/). It installs the right Python and dependencies for you.

```bash
git clone https://github.com/rawmarshmellows/surviving-pat-from-product-with-solid
cd surviving-pat-from-product-with-solid
uv run marimo edit notebook.py
```

Or skip the project setup entirely and let marimo build a throwaway environment from the notebook's inline metadata:

```bash
uvx marimo edit --sandbox notebook.py
```

The notebook follows the article section by section, with Pat's messages and the memes inline. Read-only code
blocks are the exact snippets from the article; code cells are live, so edit them, break a contract, and see who
gets paged. Deliberate errors are shown as red callouts so the rest of the notebook keeps running.

## What's in here

```
notifications/              the notifications service; every version from every section lives side by side
  notifiers/                Notifier_v1 ... v7, the audited and AI notifiers, and their interfaces
  channels/                 email, SMS, push, Slack, TextBlaster and AI SMS channels
  campaigns/                the campaign runners that use a notifier
  billing/ audit_log/ ai/   credits, the compliance audit log and the AI token budget
  wiring.py                 the composition root (and the one line that changes when Pat wants email back)
notebook.py                 the marimo notebook
images/
  slack/                    Pat's Slack-style messages
  memes/                    the memes
snippets/
  manifest.toml             every code example in the article, in reading order, one gist each
  catalog.py                renders snippets and verifies they match notifications/
  gists.json                the published gist for each snippet
article/
  article.template.md       the article, with {{gist:ID}} and {{image:...}} placeholders
  article.md                the rendered article, ready for Medium
  outline.md                the plan the rewrite was built from
scripts/
  publish_gists.py          creates or updates the gists
  render_article.py         fills the gist URLs and image links into the article
  render_images.py          renders the memes and Pat's messages with headless Chrome
tests/                      runs every snippet, the notebook, and a mypy check
```

## Tests

```bash
uv run pytest
```

The tests keep the article honest:

- Every `script` snippet runs top to bottom, and each `# -> value` or `# raises: Error: message` comment in it is checked against what actually happens.
- Every `excerpt` snippet must match the classes and methods in `notifications/` exactly.
- The article must embed every snippet and every image exactly once.
- The notebook must run end to end and pass `marimo check`.
- mypy must reject a channel that never implemented `ChannelInterface`.

## Publishing the article

```bash
uv run python scripts/render_images.py     # re-render the memes and Pat's messages (needs Google Chrome)
uv run python scripts/publish_gists.py     # verifies snippets, then creates or updates one public gist each
uv run python scripts/render_article.py    # writes article/article.md with the gist URLs and images
```

Gist ids are saved in `snippets/gists.json`, so re-running the publish script updates the existing gists
instead of creating new ones. In Medium, paste each gist URL on its own line and Medium embeds it.

The memes are original illustrations (emoji, shapes and text rendered from HTML), so no third-party meme templates live in this repo.
