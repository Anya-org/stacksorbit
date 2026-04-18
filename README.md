# StacksOrbit

StacksOrbit is a CLI-first deployment and operations toolkit for Stacks / Clarity smart contracts.

It is maintained in the `Conxian/stacksorbit` repository and used in Conxian deployment workflows, but it is intended to be useful for any Stacks team that wants repeatable deploy/monitor/verify tooling.

> **Naming note:** StacksOrbit originated under **Conxian-Labs** naming. Current repository ownership and active maintenance are under **Conxian**. You may see both names in historical files and references.

![StacksOrbit TUI Screenshot](stacksorbit-tui-screenshot.svg)

## Purpose

- Build, test, deploy, monitor, and verify Clarity contracts across devnet, testnet, and mainnet.
- Produce deployment artifacts (manifests, histories) locally for traceability.

## Status

StacksOrbit is actively maintained and used in real deployment workflows.

- **Stable areas:** core deploy/monitor/verify workflow and local deployment artifact generation.
- **Evolving areas:** CLI ergonomics, dashboard UX, and ecosystem integrations as Stacks tooling changes.
- **Operational note:** mainnet usage should be treated as an operator-reviewed and gated workflow, not a one-command push.

## Maintenance expectations

- Maintainers prioritize reliability fixes and security work on the default branch (`main`) (see [SECURITY.md](SECURITY.md)).
- Feature development is roadmap-driven and best-effort; delivery timelines are not guaranteed.
- We aim to preserve compatibility in core workflows, but options in evolving areas may change between releases.
- Community contributions are welcome; review and merge cadence depends on maintainer availability (see [CONTRIBUTING.md](CONTRIBUTING.md)).

## Intended audience and scope

- Protocol engineers shipping Clarity contracts.
- Operators running deployments and monitoring environments.
- Teams standardizing deployment workflows across multiple Stacks projects.

StacksOrbit is focused on deployment orchestration and operations. It is not a replacement for contract authoring frameworks.

## Documentation

- Developer notes and operational guidance: [AGENTS.md](AGENTS.md)
- Product/architecture notes: [PRD.md](PRD.md)
- Publishing and release hygiene: [PUBLISHING.md](PUBLISHING.md), [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md)
- GitHub Pages site source: [`docs/`](docs/) (see [`scripts/sync-pages-includes.sh`](scripts/sync-pages-includes.sh))

## Governance, ownership, and security

- Ownership and review requirements: [CODEOWNERS](CODEOWNERS)
- Contributing guide: [CONTRIBUTING.md](CONTRIBUTING.md)
- Security policy and vulnerability reporting: [SECURITY.md](SECURITY.md)
- Governance model: [GOVERNANCE.md](GOVERNANCE.md)

## Quick start (local development)

```bash
pnpm install
python -m pip install -r requirements.txt
cp .env.example .env
pnpm run test:vitest
python -m pytest tests/ -q
```
