#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
includes_dir="${repo_root}/docs/_includes"

mkdir -p "${includes_dir}"
cp "${repo_root}/AGENTS.md" "${includes_dir}/AGENTS.md"
cp "${repo_root}/PRD.md" "${includes_dir}/PRD.md"
