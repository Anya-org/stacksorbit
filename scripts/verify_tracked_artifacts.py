import subprocess
import sys

def main():
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            capture_output=True,
            text=True,
            check=True
        )
        tracked_files = result.stdout.splitlines()

        # .env.example is allowed, but .env is not.
        forbidden_patterns = [
            "node_modules/",
            "results.json",
            "coverage.xml",
            "manifest-history"
        ]

        violations = []
        for file in tracked_files:
            # Explicit check for .env (but not .env.example)
            if file == ".env" or file.endswith("/.env"):
                violations.append(file)
                continue

            for pattern in forbidden_patterns:
                if pattern in file:
                    violations.append(file)
                    break

        if violations:
            print("ERROR: Tracked forbidden artifacts found:")
            for v in violations:
                print(f"  - {v}")
            sys.exit(1)

        print("Success: No forbidden artifacts are tracked.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
