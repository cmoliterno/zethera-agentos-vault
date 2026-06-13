#!/usr/bin/env python3
"""Generate a company AgentOS vault from this public kit."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def now_date() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def slugify(value: str) -> str:
    chars = []
    previous_dash = False
    for char in value.lower():
        if char.isalnum():
            chars.append(char)
            previous_dash = False
        elif not previous_dash:
            chars.append("-")
            previous_dash = True
    return "".join(chars).strip("-") or "company"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite existing file: {path}")
    path.write_text(content, encoding="utf-8")


def copy_runtime_scripts(target: Path, source_root: Path) -> None:
    scripts = ["vault_health_check.py", "vault_rag.py", "vault_sync.py"]
    (target / "scripts").mkdir(parents=True, exist_ok=True)
    for name in scripts:
        shutil.copy2(source_root / "scripts" / name, target / "scripts" / name)


def run_git_init(target: Path) -> None:
    try:
        subprocess.run(["git", "init"], cwd=target, check=True)
    except Exception as exc:
        print(f"warning: git init failed: {exc}", file=sys.stderr)


def agents_md(company: str, slug: str) -> str:
    return f"""# {company} Agent Instructions

These instructions are for coding agents working inside this company vault.

## Read First

Always read `docs/ai/PRIMER.md` before making operational decisions.

For a project-specific task, read:

1. `projetos/<project>/_hot.md`
2. `projetos/<project>/CONTEXT.md`
3. top of `projetos/<project>/_status.md` only when needed

## Prime Directive

Act as a senior technical partner, not a blind executor.

- preserve business context
- protect architecture
- call out risk directly
- do not invent information
- do not store secrets in the vault
- do not rewrite whole systems without mapping impact
- document meaningful state changes

## Vault Update Rule

When a session changes project state:

1. append a timestamped entry at the top of `projetos/<project>/_status.md`
2. rewrite `projetos/<project>/_hot.md`
3. run `python scripts/vault_health_check.py`
4. commit and push the vault when Git remote is configured

## Sync Rule

Before starting substantial work:

```bash
python scripts/vault_sync.py --pull-only
```

After changing vault state:

```bash
python scripts/vault_sync.py --message "status: <project>"
```

## RAG Rule

Before asking the human for broad context, search the local vault:

```bash
python scripts/vault_rag.py query --db .agentos/rag.sqlite --query "<topic>"
```

If the index is missing:

```bash
python scripts/vault_rag.py ingest --root . --db .agentos/rag.sqlite
```

## Company

- company: {company}
- vault_slug: {slug}
- generated: {now_date()}
"""


def primer_md(company: str) -> str:
    return f"""---
purpose: Compact operating system for agents.
updated: {now_date()}
---

# {company} PRIMER

## What This Vault Is

This vault is the operational memory for the company. It stores project status,
technical context, operating rules, and evidence packs so agents do not need to
rediscover context in every session.

## Decision Order

1. business value
2. technical feasibility
3. architecture and maintainability
4. customer/user impact
5. margin, effort, and support cost

## Non-Negotiables

- do not invent information
- do not hide risk
- do not store secrets in the vault
- do not change databases without a migration strategy
- do not delete legacy behavior without impact mapping
- do not treat MVP as disposable work
- do not deliver empty templates
- do not load long histories when `_hot.md` is enough

## Context Protocol

For "where are we on project X":

1. read `projetos/X/_hot.md`
2. read `projetos/X/CONTEXT.md`
3. read top 60 lines of `projetos/X/_status.md` only if needed
4. query local RAG when the topic spans multiple projects

## Project Memory Files

- `_hot.md`: current state, rewritten after state changes
- `CONTEXT.md`: stable invariants, canonical paths, process rules
- `_status.md`: append-only history, newest entry on top

## Writing Zones

| Zone | Rule |
| --- | --- |
| `projetos/<x>/_status.md` | append at top |
| `projetos/<x>/_hot.md` | rewrite after state change |
| `projetos/<x>/CONTEXT.md` | update only when invariants change |
| `.agentos/` | generated local files |
| `secrets/` | references only, never real secrets |

## Health Check

```bash
python scripts/vault_health_check.py
```

## RAG

```bash
python scripts/vault_rag.py ingest --root . --db .agentos/rag.sqlite
python scripts/vault_rag.py query --db .agentos/rag.sqlite --query "<topic>"
```
"""


def config_yaml(company: str, slug: str) -> str:
    return f"""company:
  name: "{company}"
  slug: "{slug}"

vault:
  active_projects:
    - main
  hot_stale_days: 7
  status_warn_lines: 500

rag:
  mode: "sqlite_fts5_local"
  db_path: ".agentos/rag.sqlite"
  include_globs:
    - "AGENTS.md"
    - "CLAUDE.md"
    - "docs/**/*.md"
    - "projetos/**/*.md"
    - "clientes/**/*.md"
    - "decisoes/**/*.md"
  exclude_dirs:
    - ".git"
    - ".agentos"
    - "node_modules"
    - "__pycache__"

sync:
  require_pull_before_push: true
  run_health_check_before_commit: true
"""


def hot_md(project: str) -> str:
    return f"""---
project: {project}
updated: {now_date()}
instruction: Rewrite after every session that changes project state.
---

# Hot - {project}

## Current Sprint

- Initial setup.

## Active Branches

- main

## Last Decisions

- AgentOS Vault installed as the project memory source of truth.

## Blockers / Risks

- Fill with real operational blockers.

## Next Action

- Replace this template with the real current state.
"""


def context_md(project: str) -> str:
    return f"""---
project: {project}
updated: {now_date()}
purpose: Stable project context and invariants.
---

# CONTEXT - {project}

## Canonical Paths

- repository: TBD
- production: TBD
- staging: TBD

## Stack

- language: TBD
- frontend: TBD
- backend: TBD
- database: TBD
- deploy: TBD

## Business Invariants

- TBD

## Technical Invariants

- TBD

## Process Rules

- Update `_status.md` and `_hot.md` when project state changes.
- Keep secrets out of the vault.
"""


def status_md() -> str:
    return f"""## {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%MZ')}

- Event: AgentOS Vault generated.
- Changed: Created initial company/project memory structure.
- Next step: Replace templates with real project context.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap a company AgentOS Vault.")
    parser.add_argument("--company", required=True, help="Company name")
    parser.add_argument("--target", required=True, type=Path, help="Target directory")
    parser.add_argument("--project", default="main", help="Initial project slug")
    parser.add_argument("--no-git-init", action="store_true")
    args = parser.parse_args()

    source_root = Path(__file__).resolve().parents[1]
    target = args.target.resolve()
    company = args.company.strip()
    slug = slugify(company)
    project = slugify(args.project)

    if target.exists() and any(target.iterdir()):
        raise SystemExit(f"Target exists and is not empty: {target}")

    target.mkdir(parents=True, exist_ok=True)
    (target / ".agentos").mkdir(exist_ok=True)

    write(target / "README.md", f"# {company} AgentOS Vault\n\nGenerated on {now_date()}.\n")
    write(target / "AGENTS.md", agents_md(company, slug))
    write(target / "CLAUDE.md", agents_md(company, slug))
    write(target / "docs" / "ai" / "PRIMER.md", primer_md(company))
    write(target / "config" / "agentos.yaml", config_yaml(company, slug))
    write(target / "projetos" / project / "_hot.md", hot_md(project))
    write(target / "projetos" / project / "CONTEXT.md", context_md(project))
    write(target / "projetos" / project / "_status.md", status_md())
    write(target / "clientes" / ".gitkeep", "")
    write(target / "decisoes" / ".gitkeep", "")
    write(target / "secrets" / "README.md", "# Secrets\n\nStore references only. Never store secret values here.\n")
    write(target / ".gitignore", ".env\n.env.*\n!.env.example\n.agentos/*.sqlite\n.agentos/generated/\n__pycache__/\n*.pyc\n")
    copy_runtime_scripts(target, source_root)

    if not args.no_git_init:
        run_git_init(target)

    print(f"Generated AgentOS Vault at: {target}")
    print("")
    print("Next commands:")
    print(f"  cd {target}")
    print("  python scripts/vault_health_check.py --fix")
    print("  python scripts/vault_rag.py ingest --root . --db .agentos/rag.sqlite")
    print('  python scripts/vault_rag.py query --db .agentos/rag.sqlite --query "initial setup"')
    print("  git add .")
    print('  git commit -m "bootstrap: agentos vault"')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
