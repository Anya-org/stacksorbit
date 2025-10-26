# 🚀 StacksOrbit - Enhanced Deployment Tool

> **Enhanced professional deployment tool for Stacks blockchain smart contracts with full CLI capabilities, Hiro API integration, and comprehensive monitoring system.**

[![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)](https://github.com/Anya-org/stacksorbit)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/node.js-14+-green.svg)](https://nodejs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Deploy smart contracts to Stacks blockchain with confidence** - Full CLI interface, intelligent validation, real-time monitoring, and comprehensive verification.

---

## ✨ Enhanced Features

### 🚀 Full CLI Interface
- Complete command-line interface with comprehensive options
- Batch deployment with dependency ordering
- Gas estimation and optimization
- Dry-run capabilities

### 🌐 Hiro API Integration
- Real-time network monitoring
- Transaction status tracking
- Account balance monitoring
- Contract verification

### 📊 Comprehensive Monitoring
- Real-time deployment tracking
- Network health monitoring
- Transaction confirmation waiting
- Deployment manifest generation

### 🔍 Advanced Verification
- Pre-deployment checks
- Post-deployment verification
- Contract functionality testing
- Network connectivity validation

### ⚙️ Configuration Management
- Automatic configuration validation
- Environment variable management
- Wallet generation and management
- Deployment history tracking

---

## 📦 Installation

### Prerequisites
- **Python 3.8+** with pip
- **Node.js 14+** with npm
- **Clarinet** (for contract compilation)

### Install StacksOrbit

```bash
# Clone the repository
git clone https://github.com/Anya-org/stacksorbit.git
cd stacksorbit

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install

# Install globally (optional)
npm install -g .
```

### Quick Setup

```bash
# Initialize configuration
stacksorbit init

# Or use the Python script directly
python conxian_testnet_deploy.py init --network testnet

# Install dependencies
npm run install-deps
```

---

## 🚀 Quick Start

### 1. Initialize Configuration

```bash
# Generate wallet and initialize config
stacksorbit init --network testnet

# Or use Python script
python conxian_testnet_deploy.py init --generate-wallet
```

### 2. Run Pre-deployment Checks

```bash
# Comprehensive check
stacksorbit check --verbose

# Or specific checks
stacksorbit check --env-only
stacksorbit check --network-only
stacksorbit check --compile-only
```

### 3. Deploy to Testnet

```bash
# Dry run first
stacksorbit deploy --dry-run

# Deploy specific category
stacksorbit deploy --category core

# Full deployment with monitoring
stacksorbit deploy --batch-size 5 --verbose

# Deploy with parallel processing (experimental)
stacksorbit deploy --parallel --batch-size 10
```

### 4. Monitor Deployment

```bash
# Check API status
stacksorbit monitor --api-status

# Monitor in real-time
stacksorbit monitor --follow

# Or use Python script
python deployment_monitor.py --follow --verbose
```

### 5. Verify Deployment

```bash
# Verify specific contracts
stacksorbit verify --contracts all-traits cxd-token dex-factory

# Comprehensive verification
stacksorbit verify --comprehensive

# Or use Python script
python deployment_verifier.py --comprehensive --verbose
```

---

## 📖 Usage Guide

### CLI Commands

#### `stacksorbit deploy`
Deploy contracts to Stacks network

**Options:**
- `-f, --filter <contracts>` - Comma-separated list of contracts
- `-m, --mode <mode>` - Deployment mode (full, upgrade)
- `--batch-size <size>` - Contracts per batch (default: 5)
- `--dry-run` - Test without deploying
- `--parallel` - Parallel deployment (experimental)
- `--category <category>` - Deploy specific category

**Examples:**
```bash
stacksorbit deploy --dry-run
stacksorbit deploy --category core --batch-size 3
stacksorbit deploy --parallel --batch-size 10
```

#### `stacksorbit check`
Run pre-deployment checks

**Options:**
- `--env-only` - Check only environment variables
- `--network-only` - Check only network connectivity
- `--compile-only` - Check only contract compilation
- `--deployment-only` - Check only existing deployments

**Examples:**
```bash
stacksorbit check --verbose
stacksorbit check --env-only --network-only
```

#### `stacksorbit monitor`
Monitor deployment and network status

**Options:**
- `-f, --follow` - Follow deployment progress
- `-t, --tail <lines>` - Number of log lines to show
- `--api-status` - Check Hiro API status

**Examples:**
```bash
stacksorbit monitor --api-status
stacksorbit monitor --follow --tail 100
```

#### `stacksorbit verify`
Verify deployment completeness

**Options:**
- `--contracts <list>` - Specific contracts to verify
- `--comprehensive` - Run comprehensive verification

**Examples:**
```bash
stacksorbit verify --contracts all-traits cxd-token
stacksorbit verify --comprehensive
```

#### `stacksorbit config`
Manage configuration

**Subcommands:**
- `init` - Initialize configuration file
- `validate` - Validate configuration

**Examples:**
```bash
stacksorbit config init
stacksorbit config validate
```

### Python Scripts

#### Enhanced Deployment
```bash
python enhanced_conxian_deployment.py --help
python enhanced_conxian_deployment.py --dry-run --category core
```

#### Deployment Monitor
```bash
python deployment_monitor.py --help
python deployment_monitor.py --follow --verbose
```

#### Deployment Verifier
```bash
python deployment_verifier.py --help
python deployment_verifier.py --comprehensive --contracts all-traits cxd-token
```

#### Testnet Deployer
```bash
python conxian_testnet_deploy.py --help
python conxian_testnet_deploy.py deploy --dry-run
python conxian_testnet_deploy.py monitor --follow
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in your project root:

```env
# Required Variables
DEPLOYER_PRIVKEY=your_private_key_here
SYSTEM_ADDRESS=your_stacks_address_here
NETWORK=testnet

# Optional Variables (Recommended)
HIRO_API_KEY=your_hiro_api_key
CORE_API_URL=https://api.testnet.hiro.so
STACKS_API_BASE=https://api.testnet.hiro.so

# Deployment Options
DEPLOYMENT_MODE=full
BATCH_SIZE=5
PARALLEL_DEPLOY=false
CONTRACT_FILTER=

# Monitoring Options
MONITORING_ENABLED=true
LOG_LEVEL=INFO
SAVE_LOGS=true
```

### Configuration Commands

```bash
# Initialize configuration
stacksorbit init --network testnet

# Validate configuration
stacksorbit config validate

# Generate wallet
stacksorbit wallet generate --network testnet --save
```

---

## 📊 Deployment Categories

### Core Contracts
- `all-traits` - Centralized trait definitions
- `utils-encoding` - Encoding utilities
- `utils-utils` - General utilities
- `lib-error-codes` - Error code definitions

### Token Contracts
- `cxd-token` - CXD governance token
- `cxlp-token` - CXLP liquidity token
- `cxvg-token` - CXVG utility token
- `cxtr-token` - CXTR reward token
- `cxs-token` - CXS stable token

### DEX Contracts
- `dex-factory` - DEX factory
- `dex-router` - DEX router
- `dex-pool` - DEX pool
- `dex-vault` - DEX vault
- `fee-manager` - Fee management

### Governance Contracts
- `governance-token` - Governance token
- `proposal-engine` - Proposal engine
- `timelock-controller` - Timelock controller

---

## 🌐 Network Support

### Devnet
```bash
stacksorbit deploy --network devnet --dry-run
```

### Testnet
```bash
stacksorbit deploy --network testnet --batch-size 5
```

### Mainnet
```bash
stacksorbit deploy --network mainnet --batch-size 3 --parallel
```

---

## 📈 Monitoring & Verification

### Real-time Monitoring
```bash
# Monitor API status
stacksorbit monitor --api-status

# Follow deployment logs
stacksorbit monitor --follow --tail 50

# Monitor with Python script
python deployment_monitor.py --follow --verbose
```

### Deployment Verification
```bash
# Verify specific contracts
stacksorbit verify --contracts all-traits cxd-token dex-factory

# Comprehensive verification
stacksorbit verify --comprehensive

# Verify with Python script
python deployment_verifier.py --comprehensive --verbose
```

### Network Health
```bash
# Check network status
stacksorbit monitor --api-status

# Get account information
python deployment_monitor.py --address SP2ED6H1EHHTZA1NTWR2GKBMT0800Y6F081EEJ45R
```

---

## 🧪 Testing

### Run Tests
```bash
# Run all tests
npm test

# Run Python tests
python -m pytest

# Run specific test categories
npm run test:unit
npm run test:integration
npm run test:gui
```

### Development
```bash
# Install development dependencies
pip install -r requirements.txt
npm install

# Run linting
npm run lint

# Format code
npm run format

# Run CI pipeline
npm run ci
```

---

## 📚 API Reference

### Enhanced Deployer
```python
from enhanced_conxian_deployment import EnhancedConxianDeployer

deployer = EnhancedConxianDeployer(config, verbose=True)
results = deployer.deploy_conxian(category='core', dry_run=True)
```

### Deployment Monitor
```python
from deployment_monitor import DeploymentMonitor

monitor = DeploymentMonitor(network='testnet', config=config)
api_status = monitor.check_api_status()
account_info = monitor.get_account_info(address)
```

### Deployment Verifier
```python
from deployment_verifier import DeploymentVerifier

verifier = DeploymentVerifier(network='testnet', config=config)
results = verifier.run_comprehensive_verification(['all-traits', 'cxd-token'])
```

---

## 🔒 Security

### Best Practices
- **Never commit private keys** - Add `.env` to `.gitignore`
- **Use hardware wallets** for mainnet deployments
- **Verify transactions** before broadcasting
- **Monitor gas usage** and account balances
- **Test thoroughly** on testnet before mainnet

### Security Features
- Configuration validation
- Transaction confirmation
- Gas estimation
- Network verification
- Deployment rollback capabilities

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development setup
- Code style guide
- Testing requirements
- Pull request process

### Development Setup
```bash
git clone https://github.com/Anya-org/stacksorbit.git
cd stacksorbit
pip install -r requirements.txt
npm install
npm run lint
npm test
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 🔗 Links

- **GitHub**: <https://github.com/Anya-org/stacksorbit>
- **Documentation**: <https://stacksorbit.dev>
- **Issues**: <https://github.com/Anya-org/stacksorbit/issues>
- **Discussions**: <https://github.com/Anya-org/stacksorbit/discussions>
- **NPM**: <https://www.npmjs.com/package/stacksorbit>

---

## 💬 Support

- 📖 [Documentation](https://stacksorbit.dev)
- 💬 [GitHub Discussions](https://github.com/Anya-org/stacksorbit/discussions)
- 🐛 [Report Issues](https://github.com/Anya-org/stacksorbit/issues)
- 💼 [Enterprise Support](mailto:support@anyachainlabs.com)

---

## 🎯 Roadmap

### v1.1.0 (Current)
- ✅ Full CLI interface
- ✅ Hiro API integration
- ✅ Comprehensive monitoring
- ✅ Deployment verification
- ✅ Configuration management

### v1.2.0 (Planned)
- [ ] Multi-network parallel deployment
- [ ] Advanced gas optimization
- [ ] Contract upgrade wizard
- [ ] Deployment templates
- [ ] Integration with popular CI/CD platforms

### v2.0.0 (Future)
- [ ] Web-based interface
- [ ] REST API
- [ ] Docker support
- [ ] Team collaboration features
- [ ] Advanced analytics dashboard

---

**Built with ❤️ by [Anya Chain Labs](https://anyachainlabs.com)**

*Deploy smart contracts to Stacks blockchain with confidence* 🚀
