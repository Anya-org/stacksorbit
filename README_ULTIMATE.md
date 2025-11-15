# 🚀 StacksOrbit - Ultimate Deployment Tool

> **The most advanced deployment tool for Stacks blockchain with full CLI capabilities, Hiro API integration, comprehensive monitoring, and user-friendly experience for everyone.**

[![Version](https://img.shields.io/badge/version-1.2.0-blue.svg)](https://github.com/Anya-org/stacksorbit)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/node.js-14+-green.svg)](https://nodejs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Deploy smart contracts to Stacks blockchain with confidence** - Enhanced CLI, intelligent validation, real-time monitoring, comprehensive verification, and chainhooks support.

---

## ✨ Enhanced Features

### 🎯 **Smart Category Recognition**
- **Base Layer**: Foundational contracts (traits, utilities, libraries)
- **Core Infrastructure**: Essential protocol components (engines, managers, risk systems)
- **Token System**: All token contracts (CXD, CXLP, governance tokens)
- **DEX System**: Decentralized exchange (factory, router, pools, vaults)
- **Dimensional System**: Advanced features (positions, concentrated liquidity)
- **Oracle System**: Price feeds and data (aggregators, BTC adapters)
- **Governance**: DAO and governance (proposals, timelock, voting)
- **Security**: Circuit breakers, access control, monitoring
- **Chainhooks**: Blockchain hooks and triggers
- **Enterprise**: Enterprise features and compliance

### 🔗 **Chainhooks Integration**
- Automatic chainhooks detection in contracts
- Chainhooks.toml configuration management
- Real-time hook monitoring and validation
- Integration with Stacks chainhook service

### 📊 **Advanced Monitoring Dashboard**
- Real-time deployment tracking
- Network health monitoring
- Transaction confirmation waiting
- Gas usage analytics
- Account balance monitoring
- Contract verification
- Performance metrics

### 🧪 **Comprehensive Testing**
- Pre-deployment validation
- Post-deployment verification
- Network connectivity testing
- Configuration validation
- Contract compilation checking

### 🎨 **User-Friendly Experience**
- Interactive setup wizard
- Step-by-step guidance
- Deployment templates
- Comprehensive help system
- Error recovery guides

---

## 📦 Installation

### Quick Install
```bash
# Clone and setup
git clone https://github.com/Anya-org/stacksorbit.git
cd stacksorbit

# Install all dependencies
pip install -r requirements.txt
npm install

# Initialize your project
python setup_wizard.py
```

### Prerequisites
- **Python 3.8+** with pip
- **Node.js 14+** with npm
- **Clarinet** (for contract compilation)
- **Stacks account** with STX tokens

---

## 🚀 Quick Start Guide

### 1. **Setup (5 minutes)**
```bash
# Interactive setup wizard
python setup_wizard.py

# Or use the enhanced CLI
npm run setup
```

### 2. **Test Everything (2 minutes)**
```bash
# Comprehensive system check
npm run diagnose

# Or check specific components
python ultimate_stacksorbit.py check --verbose
```

### 3. **Deploy to Testnet (10 minutes)**
```bash
# Dry run first (recommended)
python ultimate_stacksorbit.py deploy --dry-run

# Deploy with monitoring
python ultimate_stacksorbit.py deploy --category core

# Full deployment with all features
python ultimate_stacksorbit.py deploy --batch-size 5 --parallel
```

### 4. **Monitor in Real-Time**
```bash
# Launch enhanced dashboard
python enhanced_dashboard.py

# Or command-line monitoring
python ultimate_stacksorbit.py monitor --follow
```

### 5. **Verify Deployment**
```bash
# Comprehensive verification
python ultimate_stacksorbit.py verify --comprehensive

# Verify specific contracts
python ultimate_stacksorbit.py verify --contracts all-traits cxd-token dex-factory
```

---

## 📖 Complete Usage Guide

### Enhanced CLI Commands

#### 🎯 **Setup & Configuration**
```bash
# Interactive setup wizard
python setup_wizard.py

# Quick setup with template
python ultimate_stacksorbit.py deploy --template testnet_quick_start

# Initialize with wallet generation
python setup_wizard.py --generate-wallet --network testnet
```

#### 🚀 **Deployment Commands**
```bash
# Basic deployment
python ultimate_stacksorbit.py deploy

# Deploy specific category
python ultimate_stacksorbit.py deploy --category base
python ultimate_stacksorbit.py deploy --category tokens
python ultimate_stacksorbit.py deploy --category dex

# Advanced deployment options
python ultimate_stacksorbit.py deploy --batch-size 3 --parallel --verbose
python ultimate_stacksorbit.py deploy --dry-run --category dimensional

# Deploy with chainhooks
python ultimate_stacksorbit.py deploy --category chainhooks
```

#### 📊 **Monitoring Commands**
```bash
# Real-time dashboard
python enhanced_dashboard.py

# Command-line monitoring
python ultimate_stacksorbit.py monitor --follow

# API status monitoring
python ultimate_stacksorbit.py monitor --api-only

# Network health monitoring
python deployment_monitor.py --follow --verbose
```

#### 🔍 **Verification Commands**
```bash
# Comprehensive verification
python ultimate_stacksorbit.py verify --comprehensive

# Verify specific contracts
python ultimate_stacksorbit.py verify --contracts all-traits cxd-token

# Contract functionality testing
python deployment_verifier.py --comprehensive
```

#### 🔧 **Diagnostic Commands**
```bash
# Full system diagnosis
python ultimate_stacksorbit.py diagnose --verbose

# Configuration validation
python ultimate_stacksorbit.py check

# Network diagnostics
python ultimate_stacksorbit.py check --network-only
```

### Category-Based Deployment

#### **Base Layer (Foundation)**
```bash
python ultimate_stacksorbit.py deploy --category base
# Deploys: all-traits, utils-encoding, utils-utils, lib-error-codes
```

#### **Core Infrastructure**
```bash
python ultimate_stacksorbit.py deploy --category core
# Deploys: dimensional-engine, position-manager, risk systems
```

#### **Token System**
```bash
python ultimate_stacksorbit.py deploy --category tokens
# Deploys: CXD, CXLP, CXVG, governance tokens
```

#### **DEX System**
```bash
python ultimate_stacksorbit.py deploy --category dex
# Deploys: factory, router, pools, vaults, MEV protection
```

#### **Dimensional System**
```bash
python ultimate_stacksorbit.py deploy --category dimensional
# Deploys: concentrated liquidity, positions, advanced routing
```

#### **Chainhooks Integration**
```bash
python ultimate_stacksorbit.py deploy --category chainhooks
# Deploys: automation, batch processors, triggers
```

### Deployment Templates

#### **Testnet Quick Start**
Perfect for development and testing
```bash
python ultimate_stacksorbit.py deploy --template testnet_quick_start
```

#### **Mainnet Production**
Production deployment with full validation
```bash
python ultimate_stacksorbit.py deploy --template mainnet_production
```

#### **Emergency Update**
Quick deployment for critical fixes
```bash
python ultimate_stacksorbit.py deploy --template emergency_update
```

---

## 🌐 Network Support

### **Devnet (Local Testing)**
```bash
# Deploy to local devnet
python ultimate_stacksorbit.py deploy --network devnet

# Prerequisites: Local Stacks node + Clarinet devnet
clarinet devnet start
```

### **Testnet (Public Testing)**
```bash
# Deploy to testnet
python ultimate_stacksorbit.py deploy --network testnet

# Get free STX: https://explorer.stacks.co/sandbox
```

### **Mainnet (Production)**
```bash
# Deploy to mainnet (uses real STX!)
python ultimate_stacksorbit.py deploy --network mainnet --batch-size 1

# ⚠️ WARNING: This costs real STX tokens!
```

---

## 🔗 Chainhooks Integration

### **Automatic Detection**
StacksOrbit automatically detects chainhooks in your contracts:
- Contract-embedded hooks
- chainhooks.toml configuration
- Hook dependencies and requirements

### **Chainhooks Deployment**
```bash
# Deploy chainhooks with contracts
python ultimate_stacksorbit.py deploy --category chainhooks

# Monitor chainhooks activity
python deployment_monitor.py --follow --verbose
```

### **Chainhooks Validation**
```bash
# Validate chainhooks configuration
python ultimate_stacksorbit.py check --chainhooks-only

# Test chainhooks functionality
python deployment_verifier.py --chainhooks-test
```

---

## 📊 Enhanced Monitoring Dashboard

### **Real-Time Features**
- Live deployment tracking
- Network health indicators
- Transaction monitoring
- Gas usage analytics
- Account balance alerts
- Contract status verification

### **Dashboard Views**
- **Overview**: System status at a glance
- **Contracts**: Contract deployment status
- **Network**: Network health and performance
- **Transactions**: Recent transaction history
- **Analytics**: Performance metrics and insights

### **Dashboard Commands**
```bash
# Launch interactive dashboard
python enhanced_dashboard.py

# Dashboard with custom settings
python enhanced_dashboard.py --update-interval 1 --verbose
```

---

## 🧪 Testing & Verification

### **Automated Testing**
```bash
# Run all tests
npm test

# Run enhanced feature tests
python test_enhanced_features.py

# Test specific components
python -m pytest tests/ -v
```

### **Pre-Deployment Checks**
```bash
# Comprehensive validation
python ultimate_stacksorbit.py check --comprehensive

# Individual checks
python ultimate_stacksorbit.py check --env-only
python ultimate_stacksorbit.py check --network-only
python ultimate_stacksorbit.py check --compile-only
```

### **Post-Deployment Verification**
```bash
# Full verification
python ultimate_stacksorbit.py verify --comprehensive

# Verify specific categories
python ultimate_stacksorbit.py verify --contracts all-traits cxd-token dex-factory
```

---

## 🎨 User Experience Features

### **Interactive Setup Wizard**
```bash
python setup_wizard.py
```
- Step-by-step configuration
- Network selection guidance
- Wallet setup assistance
- Contract analysis
- Template selection

### **Smart Error Handling**
- User-friendly error messages
- Automatic error recovery
- Troubleshooting guides
- Configuration validation

### **Deployment Templates**
```bash
# List available templates
python ultimate_stacksorbit.py template

# Apply template
python ultimate_stacksorbit.py deploy --template testnet_quick_start
```

### **Comprehensive Help**
```bash
# Get help for any command
python ultimate_stacksorbit.py --help
python setup_wizard.py --help
python enhanced_dashboard.py --help
```

---

## 📋 Configuration

### **Environment Variables**
```env
# Required
DEPLOYER_PRIVKEY=your_private_key_here
SYSTEM_ADDRESS=your_stacks_address_here
NETWORK=testnet

# Optional (Recommended)
HIRO_API_KEY=your_hiro_api_key
CORE_API_URL=https://api.testnet.hiro.so
BATCH_SIZE=5
PARALLEL_DEPLOY=false
MONITORING_ENABLED=true
```

### **Configuration Management**
```bash
# Initialize configuration
python setup_wizard.py

# Validate configuration
python ultimate_stacksorbit.py check

# Update configuration
python ultimate_stacksorbit.py config init
```

---

## 🔧 Advanced Features

### **Gas Optimization**
```bash
# Enable gas optimization
python ultimate_stacksorbit.py deploy --gas-optimization

# Custom batch sizing
python ultimate_stacksorbit.py deploy --batch-size 3
```

### **Parallel Deployment**
```bash
# Enable parallel deployment (experimental)
python ultimate_stacksorbit.py deploy --parallel --batch-size 10
```

### **Custom Monitoring**
```bash
# Custom monitoring setup
python enhanced_dashboard.py --update-interval 1 --verbose

# Save monitoring data
python deployment_monitor.py --save-snapshots
```

---

## 🛠️ Troubleshooting

### **Common Issues**

#### **Configuration Problems**
```bash
# Diagnose configuration
python ultimate_stacksorbit.py diagnose

# Validate configuration
python ultimate_stacksorbit.py check --env-only
```

#### **Network Issues**
```bash
# Check network connectivity
python ultimate_stacksorbit.py check --network-only

# Monitor API status
python ultimate_stacksorbit.py monitor --api-status
```

#### **Deployment Failures**
```bash
# Run comprehensive diagnosis
python ultimate_stacksorbit.py diagnose --verbose

# Check deployment logs
python deployment_monitor.py --follow

# Verify contract compilation
clarinet check
```

### **Recovery Steps**
1. Run: `python ultimate_stacksorbit.py diagnose`
2. Check: Network connectivity and API status
3. Verify: Configuration and account balance
4. Review: Deployment logs and error messages
5. Contact: Support if issues persist

---

## 📚 API Reference

### **Enhanced Deployer**
```python
from enhanced_conxian_deployment import EnhancedConxianDeployer

deployer = EnhancedConxianDeployer(config, verbose=True)
results = deployer.deploy_conxian(category='core', dry_run=False)
```

### **Deployment Monitor**
```python
from deployment_monitor import DeploymentMonitor

monitor = DeploymentMonitor(network='testnet', config=config)
api_status = monitor.check_api_status()
contracts = monitor.get_deployed_contracts(address)
```

### **Chainhooks Manager**
```python
from chainhooks_manager import ChainhooksManager

manager = ChainhooksManager(network='testnet', config=config)
chainhooks = manager.analyzeChainhooks()
results = manager.deployChainhooks(chainhooks)
```

---

## 🎯 Deployment Categories

### **Base Layer (Foundation)**
- `all-traits` - Centralized trait definitions
- `utils-encoding` - Encoding utilities
- `utils-utils` - General utilities
- `lib-error-codes` - Error code definitions
- `math-lib-advanced` - Advanced mathematics
- `fixed-point-math` - Fixed point calculations

### **Core Infrastructure**
- `core-dimensional-engine` - Core dimensional engine
- `core-position-manager` - Position management
- `core-oracle-oracle-adapter` - Oracle adapter
- `risk-risk-manager` - Risk management system
- `risk-liquidation-engine` - Liquidation engine
- `risk-funding-calculator` - Funding calculations

### **Token System**
- `cxd-token` - CXD governance token
- `cxlp-token` - CXLP liquidity token
- `cxvg-token` - CXVG utility token
- `cxtr-token` - CXTR reward token
- `cxs-token` - CXS stable token
- `governance-token` - Governance token
- `token-system-coordinator` - Token coordination

### **DEX System**
- `dex-factory` - DEX factory
- `dex-factory-v2` - Enhanced DEX factory
- `dex-router` - DEX router
- `dex-multi-hop-router-v3` - Multi-hop router
- `dex-pool` - DEX pool
- `dex-vault` - DEX vault
- `fee-manager` - Fee management
- `mev-protector` - MEV protection

### **Dimensional System**
- `dim-registry` - Dimensional registry
- `dim-metrics` - Dimensional metrics
- `position-nft` - Position NFTs
- `dimensional-core` - Dimensional core
- `concentrated-liquidity-pool` - Concentrated liquidity
- `dimensional-advanced-router-dijkstra` - Advanced routing

---

## 🏆 Success Stories

### **Development Workflow**
1. **Setup**: 5 minutes with wizard
2. **Testing**: 2 minutes with dry-run
3. **Deployment**: 10 minutes to testnet
4. **Monitoring**: Real-time dashboard
5. **Verification**: Comprehensive validation

### **Production Deployment**
1. **Validation**: Full system diagnosis
2. **Testing**: Multiple dry runs
3. **Deployment**: Batched with monitoring
4. **Verification**: Complete contract testing
5. **Monitoring**: 24/7 dashboard monitoring

---

## 🤝 Contributing

### **Development Setup**
```bash
git clone https://github.com/Anya-org/stacksorbit.git
cd stacksorbit
pip install -r requirements.txt
npm install
npm run test
```

### **Testing**
```bash
# Run all tests
npm test

# Run enhanced tests
python test_enhanced_features.py

# Test specific features
python -m pytest tests/unit/
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 🔗 Links

- **GitHub**: <https://github.com/Anya-org/stacksorbit>
- **Enhanced Documentation**: <https://stacksorbit.dev/enhanced>
- **Issues**: <https://github.com/Anya-org/stacksorbit/issues>
- **Discussions**: <https://github.com/Anya-org/stacksorbit/discussions>
- **NPM**: <https://www.npmjs.com/package/stacksorbit>

---

## 💬 Support

- 📖 [Enhanced Documentation](https://stacksorbit.dev/enhanced)
- 💬 [GitHub Discussions](https://github.com/Anya-org/stacksorbit/discussions)
- 🐛 [Report Issues](https://github.com/Anya-org/stacksorbit/issues)
- 💼 [Enterprise Support](mailto:support@anyachainlabs.com)

---

## 🎯 What's New in v1.2.0

### **Enhanced CLI System**
- ✅ Full command-line interface with comprehensive options
- ✅ Interactive setup wizard with guidance
- ✅ Deployment templates for different scenarios
- ✅ Advanced configuration management

### **Smart Category Recognition**
- ✅ Automatic contract categorization (base, core, tokens, etc.)
- ✅ Dependency-aware deployment ordering
- ✅ Category-specific optimization

### **Chainhooks Integration**
- ✅ Automatic chainhooks detection
- ✅ Chainhooks.toml configuration management
- ✅ Real-time hook monitoring
- ✅ Hook validation and testing

### **Advanced Monitoring Dashboard**
- ✅ Real-time deployment tracking
- ✅ Interactive dashboard with multiple views
- ✅ Network health monitoring
- ✅ Performance analytics
- ✅ Gas usage tracking

### **Comprehensive Testing**
- ✅ Pre-deployment validation
- ✅ Post-deployment verification
- ✅ Network connectivity testing
- ✅ Configuration validation
- ✅ Contract functionality testing

### **User Experience Improvements**
- ✅ Step-by-step setup wizard
- ✅ User-friendly error messages
- ✅ Comprehensive help system
- ✅ Deployment templates
- ✅ Troubleshooting guides

---

**Built with ❤️ by [Anya Chain Labs](https://anyachainlabs.com)**

*Deploy smart contracts to Stacks blockchain with confidence - now easier than ever!* 🚀

---

## 🚀 **Ready to Deploy?**

**For Beginners:**
```bash
# 1. Interactive setup
python setup_wizard.py

# 2. Test everything
python ultimate_stacksorbit.py check

# 3. Deploy to testnet
python ultimate_stacksorbit.py deploy --dry-run
python ultimate_stacksorbit.py deploy
```

**For Developers:**
```bash
# 1. Quick setup
npm run setup

# 2. Deploy with monitoring
npm run deploy

# 3. Monitor in real-time
npm run dashboard
```

**For Production:**
```bash
# 1. Comprehensive validation
npm run diagnose

# 2. Production deployment
python ultimate_stacksorbit.py deploy --template mainnet_production

# 3. Full verification
python ultimate_stacksorbit.py verify --comprehensive
```

**🎉 Happy Deploying!**
