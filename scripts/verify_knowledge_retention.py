import os
import sys


def main():
    required_files = [
        "AGENTS.md",
        "CHANGELOG.md",
        "PRD.md",
        "README.md",
        ".jules/bolt.md",
        ".jules/palette.md",
        ".jules/sentinel.md",
    ]

    missing = []
    for f in required_files:
        if not os.path.exists(f):
            missing.append(f)

    if missing:
        print("ERROR: Missing critical knowledge retention files:")
        for m in missing:
            print(f"  - {m}")
        sys.exit(1)

    print("Success: All knowledge retention files present.")


if __name__ == "__main__":
    main()
