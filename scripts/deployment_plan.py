#!/usr/bin/env python3
"""Canonical deployment plan — aligns with lib-conxian-core::deployment::DeploymentPlan.

The Rust crate lib-conxian-core defines the canonical DeploymentPlan type at
`src/deployment.rs`. This Python module mirrors that type so the Orbit CLI can
generate, validate, and persist deployment plans that are compatible with Core's
agent-readable format.

Wire path: conxius-orbit CLI → deployment_plan.py → JSON → lib-conxian-core agents
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

DEPLOYMENT_PLAN_VERSION = "1.0.0"


@dataclass
class ContractEntry:
    """Mirrors lib-conxian-core ContractEntry."""

    name: str
    nakamoto_integrity_hash: str  # SHA-256 of contract source

    @classmethod
    def from_source(cls, name: str, source: str) -> "ContractEntry":
        h = hashlib.sha256(source.encode("utf-8")).hexdigest()
        return cls(name=name, nakamoto_integrity_hash=f"sha256:{h}")


@dataclass
class DeploymentPlan:
    """Mirrors lib-conxian-core::deployment::DeploymentPlan.

    Canonical deployment plan that Orbit generates before deploying Stacks
    contracts. The JSON output is consumable by AI agents and core verifiers
    through the `to_agent_readable()` method, matching the Rust format.
    """

    project: str
    version: str
    contracts: list[ContractEntry] = field(default_factory=list)
    created_at: str = field(default="")
    network: str = "testnet"

    def __post_init__(self) -> None:
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()

    def add_contract(self, name: str, source: str) -> None:
        """Add a contract entry with integrity hash. Matches Rust add_contract()."""
        self.contracts.append(ContractEntry.from_source(name, source))

    def to_agent_readable(self) -> str:
        """Produces agent-readable deployment summary matching Rust format.

        Format includes: project name, version, contract count, per-contract
        integrity hashes, network, and creation timestamp.
        """
        lines = [
            f"# Deployment Plan: {self.project} v{self.version}",
            f"Network: {self.network}",
            f"Created: {self.created_at}",
            f"Contracts: {len(self.contracts)}",
            "",
            "## Contract Integrity Hashes",
        ]
        for i, c in enumerate(self.contracts, 1):
            lines.append(f"  [{i:03d}] {c.name}  {c.nakamoto_integrity_hash}")

        return "\n".join(lines)

    def to_json(self) -> str:
        """Serialize as canonical JSON for storage and verification."""
        return json.dumps(
            {
                "project": self.project,
                "version": self.version,
                "network": self.network,
                "created_at": self.created_at,
                "contracts": [
                    {"name": c.name, "nakamoto_integrity_hash": c.nakamoto_integrity_hash}
                    for c in self.contracts
                ],
            },
            indent=2,
        )

    @classmethod
    def from_json(cls, data: str) -> "DeploymentPlan":
        d = json.loads(data)
        plan = cls(
            project=d["project"],
            version=d["version"],
            network=d.get("network", "testnet"),
            created_at=d.get("created_at", ""),
        )
        plan.contracts = [
            ContractEntry(name=c["name"], nakamoto_integrity_hash=c["nakamoto_integrity_hash"])
            for c in d["contracts"]
        ]
        return plan

    def save(self, path: Path) -> None:
        path.write_text(self.to_json(), encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> "DeploymentPlan":
        return cls.from_json(path.read_text(encoding="utf-8"))

    def verify_integrity(self, sources: dict[str, str]) -> list[str]:
        """Verify all contract hashes match source. Returns list of failures."""
        failures: list[str] = []
        for c in self.contracts:
            if c.name not in sources:
                failures.append(f"MISSING_SOURCE: {c.name}")
                continue
            expected = ContractEntry.from_source(c.name, sources[c.name])
            if c.nakamoto_integrity_hash != expected.nakamoto_integrity_hash:
                failures.append(
                    f"HASH_MISMATCH: {c.name} "
                    f"(expected={expected.nakamoto_integrity_hash}, "
                    f"stored={c.nakamoto_integrity_hash})"
                )
        return failures


# ── Wire point for enhanced_conxian_deployment.py ──────────────────────────

def create_plan_from_clarinet(clarinet_toml_path: Path, network: str = "testnet") -> DeploymentPlan:
    """Create a DeploymentPlan by scanning a Clarinet.toml file.

    This is the primary integration point between conxius-orbit CLI and
    lib-conxian-core's DeploymentPlan model. Reads contract definitions
    from Clarinet.toml and computes integrity hashes.
    """
    import re

    content = clarinet_toml_path.read_text(encoding="utf-8")

    # Extract project name and version from [project] section
    project = "conxian"
    version = "0.1.0"
    proj_match = re.search(r'\[project\]\s*\nname\s*=\s*"([^"]+)"', content)
    if proj_match:
        project = proj_match.group(1)

    plan = DeploymentPlan(project=project, version=version, network=network)

    # Extract contracts from [[contracts]] sections
    contract_blocks = re.findall(
        r'\[\[contracts\]\]\s*\nname\s*=\s*"([^"]+)"(?:\s*\n[^[]+?)?\s*contract_file\s*=\s*"([^"]+)"',
        content,
    )
    clarinet_dir = clarinet_toml_path.parent
    for name, contract_file in contract_blocks:
        source_path = clarinet_dir / contract_file
        if source_path.exists():
            source = source_path.read_text(encoding="utf-8")
            plan.add_contract(name, source)

    return plan
