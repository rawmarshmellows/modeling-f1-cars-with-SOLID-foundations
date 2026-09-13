"""Render article/article.template.md into the Medium-ready article/driving-change-solid-f1.md.

Every `{{gist:ID}}` placeholder becomes the gist's URL on a line of its own, which
Medium turns into an embedded gist. Run scripts/publish_gists.py first.

    uv run python scripts/render_article.py
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from snippets import catalog  # noqa: E402

TEMPLATE_PATH = catalog.ROOT / "article" / "article.template.md"
ARTICLE_PATH = catalog.ROOT / "article" / "driving-change-solid-f1.md"


def main():
    published = catalog.load_published_gists()
    missing = []

    def gist_url(match):
        snippet_id = match.group(1)
        if snippet_id not in published:
            missing.append(snippet_id)
            return match.group(0)
        return published[snippet_id]["url"]

    article = re.sub(r"\{\{gist:(\w+)\}\}", gist_url, TEMPLATE_PATH.read_text())
    if missing:
        sys.exit(f"Not published yet: {', '.join(missing)}. Run scripts/publish_gists.py first.")

    ARTICLE_PATH.write_text(article)
    print(f"Wrote {ARTICLE_PATH.relative_to(catalog.ROOT)}")


if __name__ == "__main__":
    main()
