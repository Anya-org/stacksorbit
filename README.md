# StacksOrbit

StacksOrbit is a CLI-first deployment and operations toolkit for Stacks / Clarity smart contracts.

It is maintained under the Conxian GitHub organization and is used in Conxian deployment workflows, but it is intended to be useful for any Stacks team that wants repeatable deploy/monitor/verify tooling.

The project was originally created by Anya Chain Labs and is now maintained in the Conxian repository portfolio.

![StacksOrbit TUI Screenshot](stacksorbit-tui-screenshot.svg)

## Purpose

- Build, test, deploy, monitor, and verify Clarity contracts across devnet, testnet, and mainnet.
- Produce deployment artifacts (manifests, histories) locally for traceability.

## Status

Active development.

- The CLI surface and integrations may evolve as Stacks tooling changes.
- Mainnet usage should be treated as an operator workflow (reviewed and gated), not a one-command push.

## Intended audience

- Protocol engineers shipping Clarity contracts.
- Operators running deployments and monitoring environments.
- Teams standardizing deployment workflows across multiple Stacks projects.

## Documentation

- Developer notes and operational guidance: `AGENTS.md`
- Product/architecture notes: `PRD.md`
- Publishing and release hygiene: `PUBLISHING.md`, `RELEASE_CHECKLIST.md`
- GitHub Pages site source: `docs/` (see `scripts/sync-pages-includes.sh`)

## Governance, ownership, and security

- Ownership and review requirements: `CODEOWNERS`
- Contributing: `CONTRIBUTING.md`
- Security policy: `SECURITY.md`
- Governance model: `GOVERNANCE.md`

## Quick start (local development)

```bash
pnpm install
python -m pip install -r requirements.txt
cp .env.example .env
pnpm run test:vitest
python -m pytest tests/ -q
```
