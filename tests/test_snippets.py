import re

import pytest

from snippets import catalog
from snippets.catalog import ROOT, Snippet


def test_every_snippet_matches_the_code_in_notifications():
    catalog.verify_all()


def test_the_article_embeds_every_snippet_exactly_once():
    template = (ROOT / "article" / "article.template.md").read_text()
    embedded = re.findall(r"\{\{gist:(\w+)\}\}", template)
    assert sorted(embedded) == sorted(snippet.id for snippet in catalog.load_snippets())


def test_the_article_uses_every_image_exactly_once_and_they_all_exist():
    template = (ROOT / "article" / "article.template.md").read_text()
    embedded = [path for path, _alt in re.findall(r"\{\{image:([\w/]+)\|([^}]+)\}\}", template)]
    rendered = sorted(str(path.relative_to(ROOT / "images").with_suffix("")) for path in (ROOT / "images").rglob("*.png"))
    assert sorted(embedded) == rendered


def _script(tmp_path, code):
    path = tmp_path / "snippet.py"
    path.write_text(code)
    return Snippet(id="X1", kind="script", source=str(path), filename="snippet.py", description="")


def test_a_wrong_result_annotation_fails(tmp_path):
    with pytest.raises(AssertionError, match="expected 3, got 2"):
        catalog.run_script(_script(tmp_path, "1 + 1  # -> 3\n"), {})


def test_a_wrong_exception_message_fails(tmp_path):
    code = "{}['fuel']\n# raises: KeyError: 'electricity'\n"
    with pytest.raises(AssertionError, match="got `KeyError: 'fuel'`"):
        catalog.run_script(_script(tmp_path, code), {})


def test_a_missing_exception_fails(tmp_path):
    with pytest.raises(AssertionError, match="nothing was raised"):
        catalog.run_script(_script(tmp_path, "1 + 1\n# raises: ZeroDivisionError: division by zero\n"), {})


def test_an_excerpt_that_drifts_from_notifications_fails(tmp_path):
    path = tmp_path / "excerpt.py"
    path.write_text("class Notifier_v4:\n    def connect(self):\n        self.channel.open_socket()\n")
    excerpt = Snippet(id="X2", kind="excerpt", source=str(path), filename="excerpt.py", description="")
    with pytest.raises(AssertionError, match="Notifier_v4.connect differs"):
        catalog.verify_excerpt(excerpt)
