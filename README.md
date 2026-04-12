# 🚀 StacksOrbit - Ultimate Deployment Tool

> **The most advanced deployment tool for Stacks blockchain with full CLI capabilities, Hiro API integration, comprehensive monitoring, chainhooks support, and user-friendly experience for everyone.**

[![Version](https://img.shields.io/badge/version-1.2.4-blue.svg)](https://github.com/Conxian/stacksorbit)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/node.js-14+-green.svg)](https://nodejs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Deploy smart contracts to Stacks blockchain with confidence.**

![StacksOrbit TUI Screenshot](stacksorbit-tui-screenshot.svg)

## Purpose

Provide a CLI-first toolkit for building, testing, deploying, monitoring, and verifying Stacks smart contracts.

## Status

Active development. The CLI surface and integrations may evolve as Stacks tooling and deployment patterns change.

## Ownership

Ownership and review requirements are defined in [`CODEOWNERS`](./CODEOWNERS).

## Audience

- Protocol engineers shipping Clarity smart contracts.
- Operators and maintainers running deployments and monitoring environments.
- Teams standardizing deployment workflows across multiple Stacks projects.

## Relationship to the Conxian stack

- Used as part of Conxian's contract deployment and operations workflows.
- Commonly paired with orchestration layers like `conxius-platform`.

---

## 📖 Documentation

For a complete guide to developing and using StacksOrbit, please see our new **[Agent Instructions](AGENTS.md)**. This document is the "single source of truth" for all development and deployment information.

The GitHub Pages site lives under `docs/`. Before running Jekyll locally, run `bash ./scripts/sync-pages-includes.sh` from the repository root to populate `docs/_includes/`.

## 🚀 Quick Start

To get started with local development, first install the dependencies:

```bash
pnpm install
pip install -r requirements.txt
```

Then, run the tests:

```bash
pnpm run test:vitest
```

This will run the test suite and ensure that everything is set up correctly.

---
