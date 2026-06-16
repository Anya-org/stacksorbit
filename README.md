# Conxius Orbit

Conxius Orbit is public deployment and operator tooling around the broader Conxian ecosystem.

## Purpose

Support deployment workflows, contract rollout tasks, and builder tooling tied to setup and environment coordination.

## Status

**Active development.** This repository is a public tooling surface and should be treated as deployment-oriented support infrastructure rather than the canonical protocol source of truth.

## Scope

This repository owns deployment-oriented tooling, rollout helpers, and builder workflows. It does not own canonical protocol logic, shared-core governance, or private operational records.

## Governance relation

This repository is maintained by Conxian-Labs as ecosystem tooling supporting public protocol development and operations.

## Relationship to the Conxian stack

- `Conxian` is the protocol and DAO-facing core.
- `conxian-gateway` and `conxian-nexus` provide middleware and state services around deployed systems.
- `conxius-platform` provides broader platform and environment scaffolding.

## Getting started

### Development

```bash
python -m pip install -r requirements.txt
python stacksorbit_cli.py
```

### Related documentation

- [PUBLISHING.md](./PUBLISHING.md)
- [RELEASE_CHECKLIST.md](./RELEASE_CHECKLIST.md)
- [PUBLIC_READINESS.md](./PUBLIC_READINESS.md)
- [SELF_LAUNCH_README.md](./SELF_LAUNCH_README.md)

## Security

Do not disclose vulnerabilities publicly. Use [SECURITY.md](./SECURITY.md) or `security@conxian-labs.com`.

## Policies

- [CONTRIBUTING.md](./CONTRIBUTING.md)
- [SECURITY.md](./SECURITY.md)
- [CODEOWNERS](./CODEOWNERS)
- [GOVERNANCE.md](./GOVERNANCE.md)
- [REPO_OWNERSHIP.md](./REPO_OWNERSHIP.md)
- [LICENSE](./LICENSE)

## Contact

- General: [info@conxian-labs.com](mailto:info@conxian-labs.com)
- Support: [support@conxian-labs.com](mailto:support@conxian-labs.com)
- Security: [security@conxian-labs.com](mailto:security@conxian-labs.com)

## License

MIT
