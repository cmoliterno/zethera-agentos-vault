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

The live installation prompt is part of the private mentorship material and is
not published in this repository.

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
