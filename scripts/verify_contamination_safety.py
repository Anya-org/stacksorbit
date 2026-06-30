import os
import sys
import re


def main():
    # Check for direct private key exposure in scripts/tests
    secret_patterns = [
        r"(?i)private_key\s*=\s*['\"][0-9a-f]{64,66}['\"]",
        r"(?i)mnemonic\s*=\s*['\"][a-z ]{20,}['\"]",
    ]

    # Common test strings that are NOT real secrets
    safe_strings = [
        "cute bird surprise",
        "1" * 64,
        "discover unit test",
        "test test test test test test test test test test test junk",
        "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about",
    ]

    violations = []
    for root, dirs, files in os.walk("."):
        if "node_modules" in dirs:
            dirs.remove("node_modules")
        if ".git" in dirs:
            dirs.remove(".git")

        for file in files:
            if file.endswith(
                (".py", ".js", ".ts", ".clar", ".json", ".yaml", ".yml", ".toml")
            ):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", errors="ignore") as f:
                        content = f.read()
                        for pattern in secret_patterns:
                            matches = re.finditer(pattern, content)
                            for match in matches:
                                matched_str = match.group(0)
                                is_safe = any(
                                    safe_str in matched_str for safe_str in safe_strings
                                )
                                if not is_safe:
                                    violations.append(f"{path}: Matched {matched_str}")
                except Exception:
                    continue

    if violations:
        print("ERROR: Potential secret contamination found:")
        for v in violations:
            print(f"  - {v}")
        sys.exit(1)

    print("Success: No obvious secret contamination found.")


if __name__ == "__main__":
    main()
