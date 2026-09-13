"""Render article/article.template.md into the Medium-ready article/article.md.

- `{{gist:ID}}` becomes the gist's URL on a line of its own, which Medium turns into an embedded gist.
- `{{image:memes/s_drake|alt text}}` becomes a Markdown image pointing at the PNG on GitHub.

Run scripts/publish_gists.py first.

    uv run python scripts/render_article.py
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from snippets import catalog  # noqa: E402

TEMPLATE_PATH = catalog.ROOT / "article" / "article.template.md"
ARTICLE_PATH = catalog.ROOT / "article" / "article.md"
IMAGE_BASE_URL = "https://raw.githubusercontent.com/rawmarshmellows/surviving-pat-from-product-with-solid/master/images"


def main():
    published = catalog.load_published_gists()
    missing = []

    def gist_url(match):
        snippet_id = match.group(1)
        if snippet_id not in published:
            missing.append(snippet_id)
            return match.group(0)
        return published[snippet_id]["url"]

    def image(match):
        path, alt = match.group(1), match.group(2)
        if not (catalog.ROOT / "images" / f"{path}.png").is_file():
            missing.append(f"images/{path}.png")
        return f"![{alt}]({IMAGE_BASE_URL}/{path}.png)"

    article = TEMPLATE_PATH.read_text()
    article = re.sub(r"\{\{gist:(\w+)\}\}", gist_url, article)
    article = re.sub(r"\{\{image:([\w/]+)\|([^}]+)\}\}", image, article)
    if missing:
        sys.exit(f"Missing: {', '.join(missing)}. Publish the gists and render the images first.")

    ARTICLE_PATH.write_text(article)
    print(f"Wrote {ARTICLE_PATH.relative_to(catalog.ROOT)}")


if __name__ == "__main__":
    main()
