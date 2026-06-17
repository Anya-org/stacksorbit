import os
import re


def rebuild_clarinet_toml(project_dir: str):
    """
    Scans all contracts in the `contracts` directory, extracts their dependencies,
    and rebuilds the Clarinet.toml file with strict clarity 4 principles.
    """
    contracts_dir = os.path.join(project_dir, "contracts")

    # 1. Find all .clar files
    clar_files = []
    for root, dirs, filenames in os.walk(contracts_dir):
        for f in filenames:
            if f.endswith(".clar"):
                clar_files.append(os.path.join(root, f))

    # 2. Extract traits and dependencies
    dependencies = {}
    for path in clar_files:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        name = os.path.basename(path).replace(".clar", "")
        deps = set()

        for match in re.finditer(r"contract-call\?\s+\.([a-zA-Z0-9_-]+)", content):
            deps.add(match.group(1))
        for match in re.finditer(r"impl-trait\s+\.([a-zA-Z0-9_-]+)", content):
            deps.add(match.group(1))
        for match in re.finditer(
            r"use-trait\s+[a-zA-Z0-9_-]+\s+\.([a-zA-Z0-9_-]+)", content
        ):
            deps.add(match.group(1))

        if name in deps:
            deps.remove(name)

        rel_path = os.path.relpath(path, project_dir).replace("\\", "/")
        dependencies[name] = {"path": rel_path, "deps": list(deps)}

    # 3. Rebuild TOML Content
    # Official Clarity 4 config: clarity_version = 4, epoch = "latest"
    # Ref: https://docs.stacks.co/clarinet/project-structure
    toml_lines = [
        "[project]",
        'name = "StacksOrbit"',
        "authors = []",
        'description = ""',
        "telemetry = false",
        "requirements = []",
        'clarinet_version = "3.12.0"',
        'epoch = "latest"',
        "",
        "[accounts]",
        'deployer = "ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM"',
        "",
        "[simnet]",
        'mnemonic = "cute bird surprise boring old news cake design aisle helmet choose tree"',
        "",
        "[repl.analysis]",
        'passes = ["check_checker"]',
        "",
        "[repl.analysis.check_checker]",
        "strict = false",
        "trusted_sender = false",
        "trusted_caller = false",
        "callee_filter = false",
        "",
    ]

    for name, data in dependencies.items():
        toml_lines.append(f"[contracts.{name}]")
        toml_lines.append(f'path = "{data["path"]}"')
        toml_lines.append(f"clarity_version = 4")
        toml_lines.append(f'epoch = "latest"')
        if data["deps"]:
            deps_str = ", ".join([f'"{d}"' for d in data["deps"]])
            toml_lines.append(f"depends_on = [{deps_str}]")
        toml_lines.append("")

    # 4. Save Clarinet.toml
    output_path = os.path.join(project_dir, "Clarinet.toml")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(toml_lines))


if __name__ == "__main__":
    target_project = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
    rebuild_clarinet_toml(target_project)
