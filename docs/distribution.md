# Distribution Strategy

## Public But Restricted

GitHub has two practical visibility modes:

- public: anyone can view and clone
- private: only invited users can view and clone

There is no strong "public but only mentees can use" control. A license can
restrict legal/commercial use, but it cannot technically prevent cloning.

## Recommended Product Packaging

Use a three-layer model.

### Layer 1: Public Core

This repository.

Contains:

- the philosophy
- installer
- base vault structure
- local health check
- local lexical RAG
- public teaching documentation

Purpose:

- trust
- class onboarding
- fast installation
- marketing proof

### Layer 2: Private Cohort Materials

Private repo, Notion page, or gated course area.

Contains:

- client examples
- advanced prompts
- enterprise setup recordings
- support scripts
- troubleshooting playbooks

Purpose:

- protect mentorship value
- keep examples private
- avoid public leakage of operational methods

### Layer 3: Enterprise Implementation

Client-specific private repository.

Contains:

- company vault
- project memory
- internal procedures
- team-specific rules
- private RAG indexes
- integration credentials in proper secret stores

Purpose:

- actual production use
- governance
- auditability
- client confidentiality

## Licensing Recommendation

Keep this repository source-available with a restrictive commercial license
until the product strategy is settled.

If broad adoption becomes desirable later, split:

- `agentos-vault-core`: permissive open-source
- `agentos-vault-pro`: private/commercial
- `agentos-vault-enterprise`: paid implementation

