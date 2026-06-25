ConxiusOrbit is intended to be a public-facing Stacks / Clarity deployment tool.

This document tracks a small set of changes needed to keep the repository "public-ready" (clear landing docs, governance files present, CI consistent with the lockfile, and no operational artifacts committed).

## Current posture

- Landing documentation: `README.md`
- Ownership: `CODEOWNERS`
- Governance: `GOVERNANCE.md`
- Security policy: `SECURITY.md`

## Public readiness checklist

- Ensure the README describes purpose, status, and intended audience (and avoids internal-only process language).
- Keep CI aligned with the repo toolchain (`pnpm-lock.yaml` implies CI should use `pnpm`).
- Never commit secret material (private keys, mnemonics, tokens) or secret-bearing env files.
- Never commit runtime deployment artifacts (manifests / histories under `deployment/` or `.conxius_orbit/`).
- Ensure release automation references the canonical documentation site (`https://conxian.github.io/conxius_orbit/`).
