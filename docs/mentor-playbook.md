# Mentor Playbook

## Class Outcome

By the end of the class, the student should have:

- a company vault generated locally
- agent rules installed inside the vault
- at least one project memory folder
- health check passing with 0 critical issues
- local RAG index working
- first Git commit created

## Live Prompt

```text
You are helping me install Zethera AgentOS Vault for my company.

Clone the public repository:
https://github.com/cmoliterno/zethera-agentos-vault

Then run the bootstrap script for company "<COMPANY_NAME>" into
"<TARGET_PATH>".

After installation:
1. run the health check with --fix
2. ingest the local RAG index
3. run a test query
4. create the first git commit
5. do not add secrets
6. if GitHub auth is missing, stop before push and tell me the exact next step
```

## Teaching Script

1. Explain that agents fail when context is scattered.
2. Show that `AGENTS.md` gives the agent a predictable operating contract.
3. Explain that `PRIMER.md` is the compact system prompt for the company.
4. Explain `_hot.md` vs `_status.md`.
5. Run the health check.
6. Run RAG ingest and query.
7. Commit the generated vault.
8. Discuss where Notion/Obsidian fit as optional interfaces.

## Common Objections

### Why not just Notion?

Notion is good for human-facing documentation, but less ideal as the agent
runtime source of truth. Git gives diff, review, branches, rollback, CI, and
local operation.

### Why not just Obsidian?

Obsidian is a good editor. It should not be the product dependency. The product
is the versioned operating vault.

### Why not load all docs every time?

Because repeated context is expensive and noisy. The vault keeps a short hot
state and stores full history separately.

