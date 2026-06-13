#!/usr/bin/env python3
"""Git sync wrapper for AgentOS Vault."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str], dry_run: bool) -> int:
    print("+ " + " ".join(cmd))
    if dry_run:
        return 0
    completed = subprocess.run(cmd, cwd=ROOT)
    return completed.returncode


def ensure_ok(code: int, step: str) -> None:
    if code != 0:
        raise SystemExit(f"Step failed: {step}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--message", default="status: update vault")
    parser.add_argument("--pull-only", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    ensure_ok(run(["git", "pull", "--ff-only"], args.dry_run), "git pull")
    if args.pull_only:
        return 0

    ensure_ok(run([sys.executable, "scripts/vault_health_check.py"], args.dry_run), "health check")
    ensure_ok(run(["git", "status", "--short"], args.dry_run), "git status")
    ensure_ok(run(["git", "add", "."], args.dry_run), "git add")
    ensure_ok(run(["git", "commit", "-m", args.message], args.dry_run), "git commit")
    ensure_ok(run(["git", "push"], args.dry_run), "git push")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

