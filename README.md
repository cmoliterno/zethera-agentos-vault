# Zethera AgentOS Vault

Operational memory system for Claude, Codex, and other coding agents.

This repository is a public teaching and installation kit for companies that
want AI agents to work with less repeated context, clearer rules, and a safer
handoff process.

## What This Is

AgentOS Vault is not an Obsidian template and not a Notion workspace.

It is a versioned operational vault:

- agent instructions through `AGENTS.md` and `CLAUDE.md`
- a compact `docs/ai/PRIMER.md` to avoid loading long documents every session
- project memory through `_hot.md`, `CONTEXT.md`, and `_status.md`
- a health check that detects stale or missing operating files
- a local lexical RAG index for low-cost context retrieval
- sync helpers that force `pull -> check -> commit -> push`

The vault can be edited with Obsidian, VS Code, Cursor, Notion exports, or any
plain text editor. Git is the source of truth.

## Public Repo, Controlled Use

GitHub does not support "public but only selected people can clone".

If this repository is public, anyone can view and clone it. To keep commercial
control, use one of these models:

- public docs + restrictive license + private cohort support
- public bootstrap + private premium modules
- private repository with invited mentees
- public source + paid implementation/service contract

This repo starts with the first model: public educational core, commercial use
controlled by license and service delivery.

## Authorized Installation

Installation is delivered inside Zethera mentorships and implementation
engagements. The public repository documents the operating model; cohort prompts,
guided setup steps, and company-specific rollout material are distributed only to
authorized participants.

## Operating Model

The agent reads context in this order:

1. `AGENTS.md` or `CLAUDE.md`
2. `docs/ai/PRIMER.md`
3. `projetos/<project>/_hot.md`
4. `projetos/<project>/CONTEXT.md`
5. top of `projetos/<project>/_status.md` only when needed
6. local RAG evidence pack when the question is broader than one project

This keeps daily context small while preserving full history.

## Repository Layout

```text
.
├── docs/
│   ├── architecture.md
│   ├── distribution.md
│   └── mentor-playbook.md
├── scripts/
│   ├── bootstrap_vault.py
│   ├── vault_health_check.py
│   ├── vault_rag.py
│   └── vault_sync.py
├── .github/workflows/
│   └── health-check.yml
├── LICENSE.md
└── README.md
```

Generated company vaults use this structure:

```text
company-agentos-vault/
├── AGENTS.md
├── CLAUDE.md
├── docs/ai/PRIMER.md
├── config/agentos.yaml
├── projetos/<project>/_hot.md
├── projetos/<project>/CONTEXT.md
├── projetos/<project>/_status.md
├── scripts/
└── .agentos/
```

## Product Boundary

Core:

- Git-backed operational memory
- agent instruction files
- project memory protocol
- local RAG
- health checks
- sync discipline

Optional interfaces:

- Obsidian for markdown editing
- Notion or Confluence for executive documentation
- GitHub/GitLab/Bitbucket for governance
- Supabase/Postgres pgvector for shared semantic retrieval

## Security Rules

- Never store API keys, passwords, cookies, service role keys, or personal tokens
  in the vault.
- Store references to secrets, not secret values.
- Use `.env.local`, a company password manager, GitHub Actions secrets, or cloud
  secret managers.
- Treat `AGENTS.md` as executable instruction context. Review it like code.

## Minimum Acceptance Criteria

A company installation is usable when:

- `python scripts/vault_health_check.py` returns 0 critical issues
- `AGENTS.md`, `CLAUDE.md`, and `docs/ai/PRIMER.md` exist
- every active project has `_hot.md`, `CONTEXT.md`, and `_status.md`
- local RAG can ingest and return at least one evidence pack
- `python scripts/vault_sync.py --dry-run` shows the expected Git workflow
