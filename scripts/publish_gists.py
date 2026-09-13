"""Create or update one public gist per snippet in snippets/manifest.toml.

Gist ids are recorded in snippets/gists.json, so running this again updates the
existing gists in place instead of creating duplicates. Snippets are verified
against notifications/ before anything is published.

    uv run python scripts/publish_gists.py             # publish every snippet
    uv run python scripts/publish_gists.py S1 L4       # publish some snippets
    uv run python scripts/publish_gists.py --dry-run   # show what would change

Requires the GitHub CLI (`gh`), logged in to the account that should own the gists.
"""

import argparse
import contextlib
import io
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from snippets import catalog  # noqa: E402


def gh_api(method, endpoint, payload=None):
    command = ["gh", "api", "--method", method, endpoint]
    if payload is not None:
        command += ["--input", "-"]
    result = subprocess.run(
        command,
        input=json.dumps(payload) if payload is not None else None,
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def publish(snippet, published, dry_run):
    content = snippet.content()
    record = published.get(snippet.id)

    if record is None:
        print(f"{snippet.id:>4}  create  {snippet.filename}")
        if dry_run:
            return
        gist = gh_api(
            "POST",
            "/gists",
            {
                "description": snippet.description,
                "public": True,
                "files": {snippet.filename: {"content": content}},
            },
        )
    else:
        gist = gh_api("GET", f"/gists/{record['gist_id']}")
        files = gist["files"]
        unchanged = (
            gist["description"] == snippet.description
            and list(files) == [snippet.filename]
            and files[snippet.filename]["content"] == content
        )
        if unchanged:
            print(f"{snippet.id:>4}  ok      {snippet.filename}")
            return
        print(f"{snippet.id:>4}  update  {snippet.filename}")
        if dry_run:
            return
        stale_files = {name: None for name in files if name != snippet.filename}
        gist = gh_api(
            "PATCH",
            f"/gists/{record['gist_id']}",
            {
                "description": snippet.description,
                "files": {**stale_files, snippet.filename: {"content": content}},
            },
        )

    published[snippet.id] = {"gist_id": gist["id"], "url": gist["html_url"], "filename": snippet.filename}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("ids", nargs="*", help="snippet ids to publish (default: all)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    print("Verifying snippets against notifications/ ...")
    with contextlib.redirect_stdout(io.StringIO()):
        catalog.verify_all()

    snippets = catalog.load_snippets()
    unknown = set(args.ids) - {snippet.id for snippet in snippets}
    if unknown:
        parser.error(f"unknown snippet ids: {', '.join(sorted(unknown))}")

    published = catalog.load_published_gists()
    manifest_order = [snippet.id for snippet in snippets]
    try:
        for snippet in snippets:
            if not args.ids or snippet.id in args.ids:
                publish(snippet, published, args.dry_run)
    finally:
        if not args.dry_run:
            ordered = {snippet_id: published[snippet_id] for snippet_id in manifest_order if snippet_id in published}
            catalog.PUBLISHED_GISTS_PATH.write_text(json.dumps(ordered, indent=2) + "\n")


if __name__ == "__main__":
    main()
