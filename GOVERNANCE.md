# Governance

StacksOrbit is a deployment and operations toolkit for Stacks / Clarity smart contracts.

This repository is maintained under the Conxian organization. Public-facing documentation should avoid embedding operational secrets, private infrastructure identifiers, or private key material.

## Ownership

- Repo owners: defined by `CODEOWNERS`.
- Security and policy owners: `CODEOWNERS` is authoritative for changes to `SECURITY.md`, `GOVERNANCE.md`, and other governance artifacts.

## Contribution model

All changes land via pull request and should:

- Keep `.env` and other secret-bearing files out of Git.
- Avoid committing deployment artifacts (for example, `deployment/*.json`, `.stacksorbit/*`).
- Update `CHANGELOG.md` when user-facing behavior or security posture changes.

## Branches

- `main`: default branch.
- `develop`: development branch (when used).
