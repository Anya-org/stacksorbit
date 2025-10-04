# Minimal GUI smoke test for CI environments.
# This script is invoked directly by GitHub Actions (not via pytest).
# It must exit with code 0 if import paths are sane.

import sys


def main() -> None:
    # Do not launch GUI in CI; just assert module loads.
    try:
        import stacksorbit  # noqa: F401
    except Exception as e:
        print(f"Import error: {e}")
        sys.exit(1)
    print("GUI smoke test passed.")


if __name__ == "__main__":
    main()
