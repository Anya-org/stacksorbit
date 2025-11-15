# StacksOrbit Agent Instructions

Welcome to StacksOrbit! This document provides a comprehensive guide for developers and AI agents working on this project. It is the "single source of truth" for all development and deployment information.

## 1. Project Overview

StacksOrbit is an advanced deployment tool for the Stacks blockchain. It provides a full-featured command-line interface (CLI), integration with the Hiro API, comprehensive monitoring, and support for chainhooks. The goal of this project is to provide a user-friendly and powerful tool for deploying smart contracts to the Stacks blockchain with confidence.

### 1.1. Architectural Overview

StacksOrbit is a modular, command-line-driven tool for deploying and managing Stacks-based smart contracts. The following diagram illustrates the high-level architecture of the system:

```
[ User ] -> [ CLI (`stacksorbit_cli.py`) ] -> [ Core Deployer ] -> [ Stacks Blockchain ]
   |                                              ^
   |                                              |
   +-----> [ Monitoring Dashboard ] <-------------+
```

*   **User:** The developer or operator interacting with the tool.
*   **CLI (`stacksorbit_cli.py`):** The primary entry point for all commands. It parses user input and delegates tasks to the appropriate modules.
*   **Core Deployer:** The heart of the system, responsible for orchestrating the deployment process.
*   **Monitoring Dashboard:** A separate process that provides a real-time view of the deployment and network status.
*   **Stacks Blockchain:** The target network for all deployments.

### 1.2. Core Components & Terminology

The StacksOrbit project is composed of the following key components:

*   **`stacksorbit_cli.py` (formerly `ultimate_stacksorbit.py`):** The primary command-line interface for interacting with the StacksOrbit tool. The "ultimate" terminology was used to signify that this is the main, all-in-one entry point for the tool.
*   **`stacksorbit_dashboard.py` (formerly `enhanced_dashboard.py`):** A real-time, interactive dashboard for monitoring the deployment process, network health, and other key metrics. The "enhanced" terminology was used to highlight the advanced, real-time nature of the dashboard.
*   **Core Deployer (`enhanced_conxian_deployment.py`):** The main engine for deploying smart contracts. It includes features for smart category recognition, dependency ordering, and parallel deployment.
*   **Chainhooks Manager (`chainhooks_manager.py`):** This component is responsible for detecting, managing, and deploying chainhooks.
*   **Setup Wizard (`setup_wizard.py`):** An interactive wizard to guide users through the initial setup and configuration of the project.

### 1.2. Features

*   **Smart Category Recognition:** Automatically categorizes and deploys smart contracts.
*   **Chainhooks Integration:** Detects, manages, and deploys chainhooks.
*   **Advanced Monitoring Dashboard:** A real-time, interactive dashboard for monitoring deployments.
*   **Comprehensive Testing & Verification:** A full suite of tests to ensure the reliability of the tool.
*   **User-Friendly Experience:** An interactive setup wizard and clear, concise documentation.

## 2. Getting Started

### 2.1. Prerequisites

*   Python 3.8+
*   Node.js 14+
*   Git
*   Clarinet (for contract compilation)
*   A Stacks account with STX tokens

### 2.2. Installation & Setup

```bash
# Clone the repository
git clone https://github.com/Anya-org/stacksorbit.git
cd stacksorbit

# Install Python and Node.js dependencies
pip install -r requirements.txt
npm install

# Run the interactive setup wizard
python setup_wizard.py
```

### 2.3. Configuration

1.  Create a `.env` file in the root of the project.
2.  Add the following required environment variables:

```env
# Required Variables
DEPLOYER_PRIVKEY=your_private_key_here
SYSTEM_ADDRESS=your_stacks_address_here
NETWORK=testnet
```

## 3. Development

### 3.1. Development Setup

For development, it's recommended to install the Python dependencies in editable mode with the `dev` and `test` extras:

```bash
# Install Python dependencies for development
pip install -e ".[dev,test]"
```

### 3.2. Running Tests

To run the full test suite, use the following command:

```bash
npm test
```

To run specific tests:

```bash
# Python unit tests
pytest tests/unit/

# Python integration tests
pytest tests/integration/

# GUI tests
python tests/test_gui.py
```

To check test coverage:

```bash
pytest --cov=stacksorbit --cov-report=html
```

### 3.3. Code Style

*   **Python:** This project follows the [PEP 8](https://pep8.org/) style guide and uses [Black](https://black.readthedocs.io/) for formatting.
    ```bash
    # Format code
    black stacksorbit.py

    # Lint
    pylint stacksorbit.py

    # Type check
    mypy stacksorbit.py
    ```
*   **JavaScript:** This project follows the [StandardJS](https://standardjs.com/) style guide.
    ```bash
    # Lint
    npm run lint
    ```

## 4. Key Commands

The primary interface for the StacksOrbit tool is the `stacksorbit_cli.py` script. Here are some of the most common commands:

### 4.1. Setup

*   **Interactive Setup Wizard:**
    ```bash
    python setup_wizard.py
    ```

### 4.2. Deployment

*   **Dry Run (Recommended before any deployment):**
    ```bash
    python stacksorbit_cli.py deploy --dry-run
    ```
*   **Deploy to Testnet:**
    ```bash
    python stacksorbit_cli.py deploy --network testnet
    ```
*   **Deploy a Specific Category:**
    ```bash
    python stacksorbit_cli.py deploy --category core
    ```

### 4.3. Monitoring

*   **Launch the Monitoring Dashboard:**
    ```bash
    python stacksorbit_dashboard.py
    ```
*   **Monitor from the Command Line:**
    ```bash
    python stacksorbit_cli.py monitor --follow
    ```

### 4.4. Verification

*   **Comprehensive Verification:**
    ```bash
    python stacksorbit_cli.py verify --comprehensive
    ```

### 4.5. Diagnostics

*   **Full System Diagnosis:**
    ```bash
    python stacksorbit_cli.py diagnose --verbose
    ```

## 5. Contributing

### 5.1. Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/Anya-org/stacksorbit/issues)
2. If not, create a new issue with a clear title, description, and steps to reproduce.

### 5.2. Suggesting Features

1. Check [Discussions](https://github.com/Anya-org/stacksorbit/discussions) for existing suggestions.
2. Create a new discussion with a clear use case and proposed solution.

### 5.3. Pull Requests

1. **Fork** the repository.
2. **Create a branch** from `develop`.
3. **Make your changes** and **test thoroughly**.
4. **Commit** with clear messages (see "Commit Messages" section).
5. **Push** to your fork and **open a Pull Request** to the `develop` branch.

### 5.4. Pull Request Process

1. **Update documentation** if needed.
2. **Add tests** for new features.
3. **Ensure all tests pass**.
4. **Update CHANGELOG.md**.
5. **Request review** from maintainers.

## 6. Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

## 7. Release Process

1. Version bump in `package.json` and `setup.py`.
2. Update `CHANGELOG.md`.
3. Create git tag: `v1.x.x`.
4. Push tag: `git push origin v1.x.x`.
5. GitHub Actions handles publishing.

## 8. License

This project is licensed under the MIT License. See the `LICENSE` file for details.
