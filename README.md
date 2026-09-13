# Modeling F1 cars with SOLID foundations

SOLID principles in Python, told through seven decades of Formula One regulation changes.
This is the companion repo for the article **Driving Change: SOLID Principles in Python, Told Through an F1 Car**.

| Principle             | F1 moment                          | What breaks, and what fixes it                                     |
|-----------------------|------------------------------------|--------------------------------------------------------------------|
| Single Responsibility | 1951, Alfa Romeo 159               | A car that builds its own engine can't have the engine tested alone |
| Open/Closed           | 1954, 2.5L engine rules            | Swapping the engine means editing the car, until parts are injected |
| Dependency Inversion  | Mid-1980s turbo era                | An engine that starts differently crashes on the grid, until both sides depend on `EngineInterface` |
| Liskov Substitution   | 2014 hybrid era                    | A hurried hybrid subclass breaks every rule, until it keeps the parent's promises |
| Interface Segregation | Heritage demo day                  | One fat interface forces fake methods, until it's split per capability |

## Run it

You need [uv](https://docs.astral.sh/uv/getting-started/installation/). It installs the right Python and dependencies for you.

```bash
git clone https://github.com/rawmarshmellows/modeling-f1-cars-with-SOLID-foundations
cd modeling-f1-cars-with-SOLID-foundations
uv run marimo edit notebook.py
```

Or skip the project setup entirely and let marimo build a throwaway environment from the notebook's inline metadata:

```bash
uvx marimo edit --sandbox notebook.py
```

The notebook follows the article section by section. Read-only code blocks are the exact snippets from the
article; code cells are live, so edit them, break a contract, and see what happens. Deliberate errors are
shown as red callouts so the rest of the notebook keeps running.

## What's in here

```
app/                    the F1 car models; every version from every section lives side by side
  f1_cars/              F1Car_v1 ... v6, the telemetry and hybrid cars, and their interfaces
  engine/ drivers/ ...  the parts, drivers and factories
  garage.py             the composition root used by later examples
notebook.py             the marimo notebook
snippets/
  manifest.toml         every code example in the article, in reading order, one gist each
  catalog.py            renders snippets and verifies they match app/
  gists.json            the published gist for each snippet
article/
  article.template.md   the article, with {{gist:ID}} placeholders
  driving-change-solid-f1.md   the rendered article, ready for Medium
scripts/
  publish_gists.py      creates or updates the gists
  render_article.py     fills the gist URLs into the article
tests/                  runs every snippet and the whole notebook
```

## Tests

```bash
uv run pytest
```

The tests keep the article honest:

- Every `script` snippet runs top to bottom, and each `# -> value` or `# raises: Error: message` comment in it is checked against what actually happens.
- Every `excerpt` snippet must match the classes and methods in `app/` exactly.
- The article must embed every snippet exactly once.
- The notebook must run end to end and pass `marimo check`.

## Publishing the article

```bash
uv run python scripts/publish_gists.py     # verifies snippets, then creates or updates one public gist each
uv run python scripts/render_article.py    # writes article/driving-change-solid-f1.md with the gist URLs
```

Gist ids are saved in `snippets/gists.json`, so re-running the publish script updates the existing gists
instead of creating new ones. In Medium, paste each gist URL on its own line and Medium embeds it.
