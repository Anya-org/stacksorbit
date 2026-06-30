import os
import sys

def main():
    forbidden_filenames = [
        "key.pem",
        "cert.pem",
        "id_rsa",
        "id_ed25519",
        "secret.key"
    ]

    violations = []
    for root, dirs, files in os.walk("."):
        if "node_modules" in dirs:
            dirs.remove("node_modules")
        if ".git" in dirs:
            dirs.remove(".git")

        for file in files:
            if file in forbidden_filenames:
                violations.append(os.path.join(root, file))

    if violations:
        print("ERROR: Forbidden secret-bearing filenames found:")
        for v in violations:
            print(f"  - {v}")
        sys.exit(1)

    print("Success: No forbidden secret filenames found.")

if __name__ == "__main__":
    main()
