# Zethera AgentOS Vault

Operational memory kit for Claude, Codex, and other coding agents.

This repository contains the public technical core of Zethera AgentOS Vault.
Guided installation, mentorship prompts, company rollout procedures, and
commercial playbooks are distributed privately by Zethera.

## What This Is

AgentOS Vault is a versioned operating memory for AI-assisted work.

It is designed to help teams reduce repeated context, preserve project state,
and give agents a predictable operating contract.

## Public Boundary

This public repository intentionally does not include:

- classroom prompts
- full installation walkthroughs
- client rollout templates
- private implementation playbooks
- commercial operating material

Those materials live in Zethera's private mentorship workspace.

## Core Components

- vault bootstrap generator
- health check script
- local lexical RAG script
- Git sync wrapper
- source-available commercial license

## Repository Layout

```text
.
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

## Security Rules

- Never store API keys, passwords, cookies, service role keys, or personal tokens
  in the vault.
- Store references to secrets, not secret values.
- Use `.env.local`, a company password manager, GitHub Actions secrets, or cloud
  secret managers.
- Treat `AGENTS.md` as executable instruction context. Review it like code.

## Commercial Use

Commercial use, redistribution, consulting delivery, training reuse, and derived
products require written authorization from Zethera. See `LICENSE.md`.
