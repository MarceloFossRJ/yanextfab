#!/usr/bin/env python3
"""Interactive one-time setup: renames a freshly cloned copy of this template into a new
project, then removes itself. Run via `make init` or `uv run scripts/init.py`."""

from __future__ import annotations

import re
import subprocess
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

OLD_TITLE = "Yanextfab"
OLD_LOWER = "yanextfab"
OLD_OWNER_REPO = "MarceloFossRJ/yanextfab"
OLD_DOC_HOST = "marcelofossrj.github.io/yanextfab"
OLD_DB_URL_LOCAL = "postgresql+asyncpg://yanextfab:yanextfab@localhost:5432/yanextfab"
OLD_DB_URL_COMPOSE = "postgresql+asyncpg://yanextfab:yanextfab@postgres:5432/yanextfab"
OLD_SMTP_FROM = "noreply@yanextfab.dev"


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", name).strip("-").lower()
    if not slug:
        raise SystemExit("Project display name must contain at least one letter or digit.")
    return slug


def detect_github_owner_repo() -> tuple[str, str]:
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        raise SystemExit(
            "Could not read the 'origin' git remote. Make sure this is a clone of your "
            "GitHub repo (not the template's own checkout) and 'origin' is set before "
            "running this script."
        ) from exc

    url = result.stdout.strip()
    match = re.search(r"github\.com[:/]+([^/]+)/([^/.]+?)(?:\.git)?/?$", url)
    if not match:
        raise SystemExit(f"'origin' remote ({url!r}) doesn't look like a GitHub URL.")
    return match.group(1), match.group(2)


def replace_in_file(path: Path, *replacements: tuple[str, str]) -> None:
    text = path.read_text()
    for old, new in replacements:
        if old not in text:
            raise SystemExit(f"Expected text not found in {path}: {old!r}")
        text = text.replace(old, new)
    path.write_text(text)


def main() -> None:
    display_name = input('Project display name (e.g. "Acme Corp"): ').strip()
    if not display_name:
        raise SystemExit("Project display name is required.")
    description = input("Short description: ").strip()
    if not description:
        raise SystemExit("Short description is required.")
    author = input("Author name (for LICENSE): ").strip()
    if not author:
        raise SystemExit("Author name is required.")

    slug = slugify(display_name)
    db_slug = slug.replace("-", "_")
    owner, repo = detect_github_owner_repo()
    year = date.today().year
    smtp_from = f"noreply@{slug}.dev"
    doc_host = f"{owner.lower()}.github.io/{repo}"
    owner_repo = f"{owner}/{repo}"

    print("\nThis will rewrite the following derived values across the repo:")
    print(f"  Display name:       {display_name}")
    print(f"  Description:        {description}")
    print(f"  Slug:               {slug}")
    print(f"  Author / copyright: {author} ({year})")
    print(f"  GitHub owner/repo:  {owner_repo}")
    print(f"  Postgres user/db:   {db_slug}")
    print(f"  SMTP from:          {smtp_from}\n")

    if input("Proceed? [y/N] ").strip().lower() not in ("y", "yes"):
        print("Aborted. No files were changed.")
        return

    # LICENSE
    replace_in_file(
        ROOT / "LICENSE",
        ("Copyright (c) 2026 marcelofossrj", f"Copyright (c) {year} {author}"),
    )

    # README.md
    replace_in_file(
        ROOT / "README.md",
        (
            "Yet another Next.js and FastAPI boilerplate — a personal-first starter for "
            "projects that need a\nTypeScript frontend, a Python backend, and heavy "
            "AI/agent tooling out of the box.",
            description,
        ),
        (OLD_DOC_HOST, doc_host),
        (OLD_TITLE, display_name),
    )

    # frontend/README.md, backend/README.md
    for rel in ("frontend/README.md", "backend/README.md"):
        replace_in_file(
            ROOT / rel,
            (OLD_DOC_HOST, doc_host),
            (OLD_TITLE, display_name),
        )

    # mkdocs.yml
    replace_in_file(
        ROOT / "mkdocs.yml",
        (f"site_name: {OLD_TITLE}", f"site_name: {display_name}"),
        (f"repo_url: https://github.com/{OLD_OWNER_REPO}", f"repo_url: https://github.com/{owner_repo}"),
        (f"repo_name: {OLD_OWNER_REPO}", f"repo_name: {owner_repo}"),
    )

    # root pyproject.toml (docs-site tooling metadata)
    replace_in_file(
        ROOT / "pyproject.toml",
        (f'name = "{OLD_LOWER}-docs"', f'name = "{slug}-docs"'),
        (OLD_TITLE, display_name),
    )
    # Regenerate the root uv.lock so its derived `name` matches the pyproject.toml edit above.
    subprocess.run(["uv", "lock"], cwd=ROOT, check=False)

    # backend/pyproject.toml (description only — its "name" field stays "backend")
    replace_in_file(
        ROOT / "backend" / "pyproject.toml",
        (f'description = "{OLD_TITLE} FastAPI backend"', f'description = "{display_name} FastAPI backend"'),
    )

    # frontend metadata / copy / sidebar
    replace_in_file(
        ROOT / "frontend/src/app/layout.tsx",
        (f'title: "{OLD_TITLE}"', f'title: "{display_name}"'),
        (
            'description: "Yet another Next.js and FastAPI boilerplate."',
            f'description: "{description}"',
        ),
    )
    replace_in_file(
        ROOT / "frontend/src/app/register/page.tsx",
        (f"Get started with {OLD_TITLE}.", f"Get started with {display_name}."),
    )
    replace_in_file(
        ROOT / "frontend/src/components/dashboard/app-sidebar.tsx",
        (OLD_TITLE, display_name),
    )
    replace_in_file(
        ROOT / "frontend/src/lib/auth/constants.ts",
        (f'"{OLD_LOWER}_session"', f'"{db_slug}_session"'),
    )

    # backend app title / password-reset email subject
    replace_in_file(
        ROOT / "backend/src/app/main.py",
        (f'title="{OLD_TITLE} API"', f'title="{display_name} API"'),
    )
    replace_in_file(
        ROOT / "backend/src/app/core/mail.py",
        (f'subject="Reset your {OLD_TITLE} password"', f'subject="Reset your {display_name} password"'),
    )

    # Infra placeholders: docker-compose.yml
    replace_in_file(
        ROOT / "docker-compose.yml",
        ("POSTGRES_USER: yanextfab", f"POSTGRES_USER: {db_slug}"),
        ("POSTGRES_PASSWORD: yanextfab", f"POSTGRES_PASSWORD: {db_slug}"),
        ("POSTGRES_DB: yanextfab", f"POSTGRES_DB: {db_slug}"),
        ("pg_isready -U yanextfab", f"pg_isready -U {db_slug}"),
        (OLD_DB_URL_COMPOSE, f"postgresql+asyncpg://{db_slug}:{db_slug}@postgres:5432/{db_slug}"),
        (f"SMTP_FROM: {OLD_SMTP_FROM}", f"SMTP_FROM: {smtp_from}"),
    )

    # Infra placeholders: backend/.env.example
    replace_in_file(
        ROOT / "backend/.env.example",
        (OLD_DB_URL_LOCAL, f"postgresql+asyncpg://{db_slug}:{db_slug}@localhost:5432/{db_slug}"),
        (f"SMTP_FROM={OLD_SMTP_FROM}", f"SMTP_FROM={smtp_from}"),
    )

    # Infra placeholders: backend/src/app/core/config.py
    replace_in_file(
        ROOT / "backend/src/app/core/config.py",
        (
            f'database_url: str = "{OLD_DB_URL_LOCAL}"',
            f'database_url: str = "postgresql+asyncpg://{db_slug}:{db_slug}@localhost:5432/{db_slug}"',
        ),
        (f'smtp_from: str = "{OLD_SMTP_FROM}"', f'smtp_from: str = "{smtp_from}"'),
    )

    # Infra placeholders: backend/tests/conftest.py
    replace_in_file(
        ROOT / "backend/tests/conftest.py",
        (
            f'"DATABASE_URL", "{OLD_DB_URL_LOCAL}"',
            f'"DATABASE_URL", "postgresql+asyncpg://{db_slug}:{db_slug}@localhost:5432/{db_slug}"',
        ),
    )

    # Infra placeholders + CI: .github/workflows/ci.yml
    replace_in_file(
        ROOT / ".github/workflows/ci.yml",
        ("POSTGRES_USER: yanextfab", f"POSTGRES_USER: {db_slug}"),
        ("POSTGRES_PASSWORD: yanextfab", f"POSTGRES_PASSWORD: {db_slug}"),
        ("POSTGRES_DB: yanextfab", f"POSTGRES_DB: {db_slug}"),
        ("pg_isready -U yanextfab", f"pg_isready -U {db_slug}"),
        (OLD_DB_URL_LOCAL, f"postgresql+asyncpg://{db_slug}:{db_slug}@localhost:5432/{db_slug}"),
    )

    # Release workflow's repository gate
    replace_in_file(
        ROOT / ".github/workflows/release.yml",
        (f"if: github.repository == '{OLD_OWNER_REPO}'", f"if: github.repository == '{owner_repo}'"),
    )

    # Self-cleanup: remove the `init` target from the Makefile, then delete this script.
    makefile = ROOT / "Makefile"
    makefile_text = makefile.read_text()
    makefile_text = makefile_text.replace(" init", "", 1)
    makefile_text = makefile_text.replace("init:\n\tuv run scripts/init.py\n\n", "", 1)
    makefile.write_text(makefile_text)

    print("Done. scripts/init.py and the `make init` target are removing themselves now.")
    (ROOT / "scripts" / "init.py").unlink()


if __name__ == "__main__":
    main()
