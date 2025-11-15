# StacksOrbit Agent Instructions

Welcome to StacksOrbit! This document provides a comprehensive guide for developers and AI agents working on this project. It is the "single source of truth" for all development and deployment information.

## 1. Project Overview

StacksOrbit is an advanced deployment tool for the Stacks blockchain. It provides a full-featured command-line interface (CLI), integration with the Hiro API, comprehensive monitoring, and support for chainhooks. The goal of this project is to provide a user-friendly and powerful tool for deploying smart contracts to the Stacks blockchain with confidence.

### 1.1. High-Level Architecture

The StacksOrbit project is composed of the following key components:

*   **Core Deployer (`enhanced_conxian_deployment.py`):** The main engine for deploying smart contracts. It includes features for smart category recognition, dependency ordering, and parallel deployment.
*   **Chainhooks Manager (`chainhooks_manager.py`):** This component is responsible for detecting, managing, and deploying chainhooks.
*   **Monitoring Dashboard (`enhanced_dashboard.py`):** A real-time, interactive dashboard for monitoring the deployment process, network health, and other key metrics.
*   **CLI (`ultimate_stacksorbit.py`):** The primary command-line interface for interacting with the StacksOrbit tool.
*   **Setup Wizard (`setup_wizard.py`):** An interactive wizard to guide users through the initial setup and configuration of the project.

## 2. Getting Started

### 2.1. Prerequisites

*   Python 3.8+
*   Node.js 14+
*   Git
*   Clarinet (for contract compilation)
*   A Stacks account with STX tokens

### 2.2. Installation

```bash
# Clone the repository
git clone https://github.com/Anya-org/stacksorbit.git
cd stacksorbit

# Install Python and Node.js dependencies
pip install -r requirements.txt
npm install
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

For a full list of available configuration options, please see the `Configuration` section in the main `README.md`.

## 3. Development Workflow

### 3.1. Running Tests

To run the full test suite, use the following command:

```bash
npm test
```

To run specific Python tests, you can use `pytest`:

```bash
pytest tests/unit/
```

### 3.2. Code Style

*   **Python:** This project follows the [PEP 8](https://pep8.org/) style guide and uses [Black](https://black.readthedocs.io/) for formatting.
*   **JavaScript:** This project follows the [StandardJS](https://standardjs.com/) style guide.

### 3.3. Contribution Guidelines

Please see the `CONTRIBUTING.md` file for detailed instructions on how to contribute to this project.

## 4. Key Commands

The primary interface for the StacksOrbit tool is the `ultimate_stacksorbit.py` script. Here are some of the most common commands:

### 4.1. Setup

*   **Interactive Setup Wizard:**
    ```bash
    python setup_wizard.py
    ```

### 4.2. Deployment

*   **Dry Run (Recommended before any deployment):**
    ```bash
    python ultimate_stacksorbit.py deploy --dry-run
    ```
*   **Deploy to Testnet:**
    ```bash
    python ultimate_stacksorbit.py deploy --network testnet
    ```
*   **Deploy a Specific Category:**
    ```bash
    python ultimate_stacksorbit.py deploy --category core
    ```

### 4.3. Monitoring

*   **Launch the Monitoring Dashboard:**
    ```bash
    python enhanced_dashboard.py
    ```
*   **Monitor from the Command Line:**
    ```bash
    python ultimate_stacksorbit.py monitor --follow
    ```

### 4.4. Verification

*   **Comprehensive Verification:**
    ```bash
    python ultimate_stacksorbit.py verify --comprehensive
    ```

### 4.5. Diagnostics

*   **Full System Diagnosis:**
    ```bash
    python ultimate_stacksorbit.py diagnose --verbose
    ```

## 5. License

This project is licensed under the MIT License. See the `LICENSE` file for details.
