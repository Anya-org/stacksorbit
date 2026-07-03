# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### 🔄 **Development**

- Research and planning for future enhancements
- Community feedback integration
- Performance optimizations
- Additional network support

## [1.2.10] - 2026-07-03

### Added
- Scheduled CI workflow (`scheduled-tests.yml`) for weekly full system validation (Sundays).
- ADR 001: Established RGB protocol v0.11.1 ecosystem as the production target.
- Knowledge retention journals in `.jules/` (`bolt.md`, `palette.md`, `sentinel.md`).

### Changed
- Standardized Node.js version to 22 across all workflows for modern environment compatibility.
- Hardened dependency review workflow by enforcing strict policy gates (upstream aligned).

### Fixed
- Resolved repository hygiene gaps by synchronizing missing validation scripts and documentation placeholders.

## [1.2.9] - 2026-06-30

### Added
- Missing CI validation scripts: `verify_knowledge_retention.py`, `verify_tracked_artifacts.py`, `verify_contamination_safety.py`, `verify_compose_env_templates.py`, `verify_submodule_secret_filenames.py`, `verify_bos_production_boundary.py`.
- Enforced mandatory CI validation in `ci.yml`.
- Hardened `dependency-review.yml` policy (removed `continue-on-error`).

### Fixed
- Project version alignment across `package.json`, `setup.py`, and `PRD.md` to v1.2.9.
- Resolved "tracked artifacts" issue by verifying clean source control.

## [1.2.0] - 2025-11-14

### Added
- Local development network using `stacks-core`
- `devnet` command to the CLI to start, stop, and check the status of the local development network
- Installation of `stacks-core` to the setup wizard
- Configuration of `stacks-core` path in `.env` file

### Changed
- Updated `LocalDevnet` class to be stateless using a PID file
- Improved setup wizard with checks for `git` and `cargo`
- Setup wizard now streams output of long-running commands
- Corrected step numbering in the setup wizard

## [1.1.0] - 2025-10-26

### ✨ **Major Features Added**

#### 🚀 **Enhanced CLI System**
- **Complete command-line interface** with comprehensive options and subcommands
- **Interactive setup wizard** with step-by-step guidance for all skill levels
- **Deployment templates** for different scenarios (testnet, mainnet, emergency)
- **Advanced configuration management** with validation and auto-detection
- **Comprehensive help system** with detailed usage examples

#### 💰 **Wallet Balance Integration**
- **Real-time STX balance monitoring** with available funds calculation
- **Deployment cost estimation** with warnings for insufficient funds
- **Account status display** showing total, locked, and available balances
- **Smart deployment warnings** based on wallet balance and estimated costs
- **Integration across all components** (dashboard, CLI, auto-detection)

#### 🔍 **Enhanced Auto-Detection System**
- **Multi-method contract discovery** (Clarinet.toml, directory scanning, manifests)
- **Intelligent deployment planning** with full vs upgrade mode detection
- **Contract categorization** with dependency-aware deployment ordering
- **Deployment state persistence** across sessions and directory changes
- **Generic SDK 3.8 compatibility** with fallback mechanisms

#### 📊 **Advanced Monitoring Dashboard**
- **Interactive real-time dashboard** with multiple views (overview, contracts, network, transactions, analytics)
- **Network health monitoring** with performance analytics and error tracking
- **Transaction monitoring** with confirmation tracking and status updates
- **Gas usage analytics** and account balance monitoring
- **Comprehensive metrics** including API response times and uptime tracking

#### 🧪 **Comprehensive Testing & Verification**
- **Pre-deployment validation** with intelligent checks and diagnostics
- **Post-deployment verification** with contract functionality testing
- **Network connectivity testing** and API status validation
- **Configuration validation** with detailed error reporting
- **Automated error detection** and recovery suggestions

#### 🔗 **Chainhooks Integration**
- **Automatic chainhooks detection** in smart contracts
- **Chainhooks.toml configuration management** with validation
- **Real-time hook monitoring** and trigger validation
- **Integration with Stacks chainhook service** for enhanced functionality

### 🛠️ **Improvements**
- **User-friendly error messages** with actionable recovery steps
- **Comprehensive troubleshooting guides** and automated diagnostics
- **Interactive setup process** that works for beginners and experts
- **Clear deployment progress** with estimated times and costs
- **Smart recommendations** based on system analysis

### 🐛 **Bug Fixes**
- **Fixed syntax errors** in dashboard and CLI components
- **Resolved import issues** in auto-detection system
- **Fixed configuration parsing** with better error handling
- **Corrected wallet balance calculations** and display formatting
- **Fixed deployment order dependencies** in contract categorization

### 📚 **Documentation**
- **Comprehensive README** with complete usage examples
- **Enhanced API documentation** with code examples
- **Troubleshooting guides** with common issues and solutions
- **Deployment templates documentation** with use cases
- **Configuration examples** for different environments

### 🔧 **Technical Improvements**
- **SDK 3.8 compatibility** with fallback support for older versions
- **Enhanced TOML parsing** with manual fallback for maximum compatibility
- **Improved API integration** with better error handling and retry logic
- **Better dependency management** with comprehensive requirements
- **Cross-platform compatibility** improvements for Windows, macOS, Linux

### 📈 **Analytics & Monitoring**
- **Real-time performance metrics** with historical tracking
- **Error rate monitoring** with alerting thresholds
- **Deployment success tracking** with detailed analytics
- **Network health indicators** with proactive warnings
- **Resource usage monitoring** with optimization recommendations

---

## [1.0.0] - 2024-12-01

### 🚀 **Initial Release**
- Basic GUI deployment tool for Stacks blockchain
- Simple contract deployment functionality
- Basic configuration management
- Initial testnet support

### BOLT **Bolt: Performance Optimizations**
- Consolidated redundant directory scans in auto-detection into a single-pass `os.walk`.
- Implemented in-memory caching for project files and parsed JSON manifests.
- Optimized file hashing with chunked reading for memory efficiency.

---

## 📋 **Release Checklist**

For each release, ensure:
- [x] Version updated in package.json
- [x] Version updated in setup.py
- [x] Version updated in README.md
- [x] CHANGELOG.md updated with new features
- [x] All tests passing (npm test)
- [x] Documentation updated
- [x] Release notes prepared
- [x] GitHub release created
- [x] NPM package published
- [x] PyPI package published

---

**Built with ❤️ by [Conxian-Labs](https://anyachainlabs.com)**

*Deploy smart contracts to Stacks blockchain with confidence - now easier than ever!* 🚀
