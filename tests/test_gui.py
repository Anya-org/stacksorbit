# Minimal GUI smoke test for CI environments.
# This script is invoked directly by GitHub Actions (not via pytest).
# It must exit with code 0 if import paths are sane.

import sys
from pathlib import Path

# Add project root to path to allow imports of modules in root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def main() -> None:
    # Do not launch GUI in CI; just assert module loads.
    try:
        import enhanced_dashboard  # noqa: F401
        import stacksorbit  # noqa: F401
    except Exception as e:
        print(f"Import error: {e}")
        sys.exit(1)
    print("GUI smoke test passed.")


if __name__ == "__main__":
    main()
