"""Load, render and verify the code snippets listed in snippets/manifest.toml.

The same catalog feeds the gists, the article and the notebook, so all three show
exactly the code that the tests execute.
"""

import ast
import difflib
import io
import json
import tokenize
import tomllib
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "snippets" / "manifest.toml"
PUBLISHED_GISTS_PATH = ROOT / "snippets" / "gists.json"

RESULT_MARKER = "# -> "
RAISES_MARKER = "# raises: "


@dataclass(frozen=True)
class Snippet:
    id: str
    kind: str
    source: str
    filename: str
    description: str
    base: str | None = None

    @property
    def section(self):
        return self.id[0]

    @property
    def language(self):
        return "diff" if self.kind == "diff" else "python"

    def content(self):
        if self.kind == "diff":
            return _unified_diff(self.base, self.source)
        return (ROOT / self.source).read_text()


def load_snippets():
    manifest = tomllib.loads(MANIFEST_PATH.read_text())
    return [Snippet(**entry) for entry in manifest["gist"]]


def get_snippet(snippet_id):
    for snippet in load_snippets():
        if snippet.id == snippet_id:
            return snippet
    raise KeyError(f"No snippet with id {snippet_id!r} in {MANIFEST_PATH.name}")


def load_published_gists():
    if not PUBLISHED_GISTS_PATH.exists():
        return {}
    return json.loads(PUBLISHED_GISTS_PATH.read_text())


def snippet_markdown(snippet_id):
    """The snippet as a fenced code block with a caption, linking to its gist once published."""
    snippet = get_snippet(snippet_id)
    gist = load_published_gists().get(snippet_id)
    caption = f"[`{snippet.filename}`]({gist['url']})" if gist else f"`{snippet.filename}`"
    return f"```{snippet.language}\n{snippet.content()}```\n\n<small>{snippet.id} · {caption}</small>"


def _unified_diff(base, source):
    before = (ROOT / base).read_text().splitlines(keepends=True)
    after = (ROOT / source).read_text().splitlines(keepends=True)
    return "".join(difflib.unified_diff(before, after, fromfile=Path(base).name, tofile=Path(source).name))


# ---------------------------------------------------------------------------------- verification


def verify_all():
    """Raise AssertionError if any snippet has drifted from the code in notifications/."""
    snippets = load_snippets()
    ids = [snippet.id for snippet in snippets]
    assert len(ids) == len(set(ids)), f"Duplicate snippet ids in {MANIFEST_PATH.name}"

    namespaces = {}
    for snippet in snippets:
        if snippet.kind in ("file", "diff"):
            for path in filter(None, (snippet.base, snippet.source)):
                assert (ROOT / path).is_file(), f"{snippet.id}: {path} does not exist"
            assert snippet.content().strip(), f"{snippet.id}: renders to nothing"
        elif snippet.kind == "excerpt":
            verify_excerpt(snippet)
        elif snippet.kind == "script":
            run_script(snippet, namespaces.setdefault(snippet.section, {"__name__": "snippets"}))
        else:
            raise AssertionError(f"{snippet.id}: unknown kind {snippet.kind!r}")


def verify_excerpt(snippet):
    """Every class in the excerpt must have the same bases as in notifications/, and every method that isn't `...` must match."""
    source = snippet.content()
    exec(compile(source, snippet.source, "exec"), {"__name__": "snippets"})

    package_classes = _package_classes()
    for excerpt_class in _classes(ast.parse(source)):
        assert excerpt_class.name in package_classes, f"{snippet.id}: class {excerpt_class.name} is not in notifications/"
        package_class = package_classes[excerpt_class.name]
        assert _dump(excerpt_class.bases) == _dump(package_class.bases), (
            f"{snippet.id}: {excerpt_class.name} has different base classes in notifications/"
        )
        package_methods = {node.name: node for node in package_class.body if isinstance(node, ast.FunctionDef)}
        for method in excerpt_class.body:
            if not isinstance(method, ast.FunctionDef) or _is_elided(method.body):
                continue
            assert method.name in package_methods, f"{snippet.id}: {excerpt_class.name}.{method.name} is not in notifications/"
            assert _dump(method) == _dump(package_methods[method.name]), (
                f"{snippet.id}: {excerpt_class.name}.{method.name} differs from notifications/"
            )


def run_script(snippet, namespace):
    """Run a script statement by statement, checking its `# -> value` and `# raises: Error: message` annotations."""
    source = snippet.content()
    comments = _comments_by_line(source)
    lines = source.splitlines()

    for statement in ast.parse(source).body:
        annotation = _annotation_for(statement, comments, lines)
        where = f"{snippet.id} ({snippet.source}:{statement.lineno})"

        if annotation and annotation.startswith(RAISES_MARKER):
            expected = annotation.removeprefix(RAISES_MARKER)
            try:
                _exec(statement, snippet, namespace)
            except Exception as error:
                actual = f"{type(error).__name__}: {error}"
                assert actual == expected, f"{where}: expected `{expected}`, got `{actual}`"
            else:
                raise AssertionError(f"{where}: expected `{expected}`, but nothing was raised")

        elif annotation and annotation.startswith(RESULT_MARKER):
            assert isinstance(statement, ast.Expr), f"{where}: `# ->` must annotate an expression"
            expected = annotation.removeprefix(RESULT_MARKER)
            value = eval(compile(ast.Expression(statement.value), snippet.source, "eval"), namespace)
            assert repr(value) == expected, f"{where}: expected {expected}, got {value!r}"

        else:
            _exec(statement, snippet, namespace)


def _exec(statement, snippet, namespace):
    module = ast.Module(body=[statement], type_ignores=[])
    exec(compile(module, snippet.source, "exec"), namespace)


def _annotation_for(statement, comments, lines):
    """An annotation sits at the end of the statement's last line, or alone on the line after it."""
    inline = comments.get(statement.end_lineno)
    if inline and inline.startswith((RESULT_MARKER, RAISES_MARKER)):
        return inline
    next_line = lines[statement.end_lineno].strip() if statement.end_lineno < len(lines) else ""
    if next_line.startswith((RESULT_MARKER, RAISES_MARKER)):
        return next_line
    return None


def _comments_by_line(source):
    tokens = tokenize.generate_tokens(io.StringIO(source).readline)
    return {token.start[0]: token.string for token in tokens if token.type == tokenize.COMMENT}


def _package_classes():
    classes = {}
    for path in sorted((ROOT / "notifications").rglob("*.py")):
        for node in _classes(ast.parse(path.read_text())):
            assert node.name not in classes, f"Class {node.name} is defined twice in notifications/"
            classes[node.name] = node
    return classes


def _classes(tree):
    return [node for node in tree.body if isinstance(node, ast.ClassDef)]


def _is_elided(body):
    return (
        len(body) == 1
        and isinstance(body[0], ast.Expr)
        and isinstance(body[0].value, ast.Constant)
        and body[0].value.value is Ellipsis
    )


def _dump(node):
    if isinstance(node, list):
        return [ast.dump(item) for item in node]
    return ast.dump(node)
