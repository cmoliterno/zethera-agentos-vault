#!/usr/bin/env python3
"""Health check for an AgentOS Vault."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


ROOT = Path(__file__).resolve().parents[1]
PROJECTS_DIR = ROOT / "projetos"
HOT_STALE_DAYS = 7
STATUS_WARN_LINES = 500


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")


def read_updated(path: Path) -> datetime | None:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception:
        return None
    in_frontmatter = False
    for line in lines[:25]:
        if line.strip() == "---":
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter and line.startswith("updated:"):
            raw = line.split(":", 1)[1].strip().strip('"').strip("'")
            try:
                return datetime.strptime(raw[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc)
            except ValueError:
                return None
    return None


def count_lines(path: Path) -> int:
    try:
        return len(path.read_text(encoding="utf-8").splitlines())
    except Exception:
        return 0


def result(check: str, status: str, detail: str, project: str | None = None) -> dict:
    data = {"check": check, "status": status, "detail": detail}
    if project:
        data["project"] = project
    return data


def hot_template(project: str) -> str:
    return f"""---
project: {project}
updated: {now_iso()[:10]}
instruction: Rewrite after every session that changes project state.
---

# Hot - {project}

## Current Sprint

- TBD

## Active Branches

- TBD

## Last Decisions

- TBD

## Blockers / Risks

- TBD

## Next Action

- TBD
"""


def context_template(project: str) -> str:
    return f"""---
project: {project}
updated: {now_iso()[:10]}
purpose: Stable project context and invariants.
---

# CONTEXT - {project}

## Canonical Paths

- TBD

## Stack

- TBD

## Business Invariants

- TBD

## Technical Invariants

- TBD

## Process Rules

- Update `_status.md` and `_hot.md` after meaningful state changes.
"""


def status_template() -> str:
    return f"""## {now_iso()}

- Event: status file created by health check.
- Changed: generated missing `_status.md`.
- Next step: replace with real project history.
"""


def check_global() -> list[dict]:
    checks = []
    for path in ["AGENTS.md", "CLAUDE.md", "docs/ai/PRIMER.md", "config/agentos.yaml"]:
        candidate = ROOT / path
        checks.append(result(path, "ok" if candidate.exists() else "missing", "exists" if candidate.exists() else "missing"))
    return checks


def check_project(project_dir: Path, fix: bool) -> list[dict]:
    checks = []
    project = project_dir.name
    hot = project_dir / "_hot.md"
    context = project_dir / "CONTEXT.md"
    status = project_dir / "_status.md"

    if not hot.exists():
        if fix:
            hot.write_text(hot_template(project), encoding="utf-8")
            checks.append(result("_hot.md", "fixed", "created", project))
        else:
            checks.append(result("_hot.md", "missing", "missing fresh context file", project))
    else:
        updated = read_updated(hot)
        if updated and datetime.now(timezone.utc) - updated > timedelta(days=HOT_STALE_DAYS):
            checks.append(result("_hot.md", "warn", f"stale since {updated.date()}", project))
        else:
            checks.append(result("_hot.md", "ok", "exists", project))

    if not context.exists():
        if fix:
            context.write_text(context_template(project), encoding="utf-8")
            checks.append(result("CONTEXT.md", "fixed", "created", project))
        else:
            checks.append(result("CONTEXT.md", "missing", "missing stable context file", project))
    else:
        checks.append(result("CONTEXT.md", "ok", "exists", project))

    if not status.exists():
        if fix:
            status.write_text(status_template(), encoding="utf-8")
            checks.append(result("_status.md", "fixed", "created", project))
        else:
            checks.append(result("_status.md", "missing", "missing append-only history", project))
    else:
        lines = count_lines(status)
        if lines > STATUS_WARN_LINES:
            checks.append(result("_status.md", "warn", f"{lines} lines; prefer _hot.md for daily context", project))
        else:
            checks.append(result("_status.md", "ok", f"{lines} lines", project))
    return checks


def all_checks(fix: bool) -> list[dict]:
    checks = check_global()
    if not PROJECTS_DIR.exists():
        checks.append(result("projetos", "missing", "missing project directory"))
        return checks
    project_dirs = [p for p in PROJECTS_DIR.iterdir() if p.is_dir()]
    if not project_dirs:
        checks.append(result("projetos", "missing", "no project folders found"))
    for project_dir in project_dirs:
        checks.extend(check_project(project_dir, fix))
    return checks


def render(checks: list[dict]) -> str:
    lines = [f"# AgentOS Vault Health Check - {now_iso()}", ""]
    for status in ["missing", "warn", "fixed", "ok"]:
        items = [c for c in checks if c["status"] == status]
        if not items:
            continue
        lines.append(f"## {status.upper()}")
        for item in items:
            project = f"[{item['project']}] " if "project" in item else ""
            lines.append(f"- {project}{item['check']}: {item['detail']}")
        lines.append("")
    critical = len([c for c in checks if c["status"] == "missing"])
    warn = len([c for c in checks if c["status"] == "warn"])
    ok = len([c for c in checks if c["status"] == "ok"])
    fixed = len([c for c in checks if c["status"] == "fixed"])
    lines.append(f"Result: {ok} OK | {warn} warnings | {fixed} fixed | {critical} critical")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fix", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    checks = all_checks(args.fix)
    if args.as_json:
        print(json.dumps(checks, ensure_ascii=False, indent=2))
    else:
        print(render(checks))
    return 1 if any(c["status"] == "missing" for c in checks) else 0


if __name__ == "__main__":
    raise SystemExit(main())

