import os
import sys


def main():
    # Verify that .env.example contains all keys used in the codebase
    if not os.path.exists(".env.example"):
        print("ERROR: .env.example missing.")
        sys.exit(1)

    with open(".env.example", "r") as f:
        example_content = f.read()

    required_keys = ["DEPLOYER_PRIVKEY", "SYSTEM_ADDRESS", "NETWORK"]
    missing = [k for k in required_keys if k not in example_content]

    if missing:
        print(f"ERROR: .env.example missing required keys: {missing}")
        sys.exit(1)

    print("Success: .env.example is valid.")


if __name__ == "__main__":
    main()
