#!/usr/bin/env python3
"""
Enhanced StacksOrbit Auto-Detection System
Complete solution for directory change handling, contract discovery, deployment status tracking
"""

import os
import sys
import json
import time
import hashlib
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
class GenericStacksAutoDetector:
    """Generic Stacks contract auto-detector compatible with Clarinet SDK 3.8"""

    def __init__(self, project_root: Optional[Path] = None, use_conxian_mode: bool = False):
        self.project_root = project_root or Path.cwd()
        self.use_conxian_mode = use_conxian_mode  # Keep Conxian-specific features as optional
        self.contract_cache = {}
        self.deployment_cache = {}
        self.state_file = self.project_root / ".stacksorbit" / "auto_detection_state.json"
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state = self._load_state()

        # Load contract categories (generic + optional Conxian)
        self.contract_categories = self._load_contract_categories()

    def _load_contract_categories(self) -> Dict:
        """Load contract categories - generic Stacks + optional Conxian"""
        categories = {
            # Generic Stacks contract patterns (SDK 3.8 compatible)
            'traits': [
                'trait', 'traits', 'interfaces', 'interface',
                'sip-009', 'sip-010', 'sip-013', 'sip-018'
            ],
            'tokens': [
                'token', 'ft', 'nft', 'fungible', 'non-fungible',
                'mint', 'burn', 'transfer', 'balance', 'supply'
            ],
            'defi': [
                'dex', 'swap', 'pool', 'liquidity', 'amm',
                'router', 'factory', 'pair', 'vault', 'staking',
                'farming', 'yield', 'rewards', 'governance'
            ],
            'oracle': [
                'oracle', 'price', 'feed', 'aggregator', 'adapter',
                'btc', 'usd', 'eth', 'chainlink', 'pyth'
            ],
            'dao': [
                'dao', 'governance', 'proposal', 'vote', 'voting',
                'timelock', 'upgrade', 'admin', 'owner', 'controller'
            ],
            'security': [
                'auth', 'access', 'control', 'circuit', 'breaker',
                'pause', 'pausable', 'rate', 'limit', 'emergency'
            ],
            'utilities': [
                'utils', 'util', 'helper', 'library', 'lib',
                'math', 'string', 'encoding', 'crypto', 'hash'
            ],
            'testing': [
                'test', 'mock', 'fake', 'simulator', 'debug'
            ]
        }

        # Add Conxian-specific categories if in Conxian mode
        if self.use_conxian_mode:
            categories.update({
                'conxian_base': [
                    'all-traits', 'utils-encoding', 'utils-utils', 'lib-error-codes',
                    'math-lib-advanced', 'fixed-point-math', 'standard-constants'
                ],
                'conxian_tokens': [
                    'cxd-token', 'cxlp-token', 'cxvg-token', 'cxtr-token', 'cxs-token',
                    'governance-token', 'token-system-coordinator', 'token-emission-controller'
                ],
                'conxian_dex': [
                    'dex-factory', 'dex-factory-v2', 'dex-router', 'dex-pool', 'dex-vault',
                    'dex-multi-hop-router-v3', 'fee-manager', 'liquidity-manager',
                    'stable-swap-pool', 'weighted-swap-pool', 'mev-protector'
                ],
                'conxian_dimensional': [
                    'dim-registry', 'dim-metrics', 'dim-graph', 'dim-oracle-automation',
                    'dim-revenue-adapter', 'dim-yield-stake', 'position-nft',
                    'dimensional-core', 'dimensional-advanced-router-dijkstra',
                    'concentrated-liquidity-pool', 'concentrated-liquidity-pool-v2'
                ],
                'conxian_governance': [
                    'governance-token', 'proposal-engine', 'timelock-controller',
                    'upgrade-controller', 'emergency-governance', 'governance-signature-verifier'
                ],
                'conxian_oracle': [
                    'oracle', 'oracle-aggregator', 'oracle-aggregator-v2', 'btc-adapter',
                    'external-oracle-adapter', 'oracle-dimensional-oracle'
                ],
                'conxian_security': [
                    'circuit-breaker', 'pausable', 'access-control-interface',
                    'rate-limiter', 'mev-protector', 'monitoring-dashboard'
                ],
                'conxian_monitoring': [
                    'analytics-aggregator', 'monitoring-dashboard', 'finance-metrics',
                    'performance-optimizer', 'price-stability-monitor', 'system-monitor',
                    'real-time-monitoring-dashboard', 'protocol-invariant-monitor'
                ],
                'conxian_chainhooks': [
                    'batch-processor', 'keeper-coordinator', 'automation-batch-processor',
                    'transaction-batch-processor', 'predictive-scaling-system'
                ],
                'conxian_enterprise': [
                    'enterprise-api', 'enterprise-loan-manager', 'compliance-hooks',
                    'budget-manager', 'enterprise-compliance-hooks'
                ],
                'conxian_lending': [
                    'comprehensive-lending-system', 'enterprise-loan-manager',
                    'sbtc-lending-system', 'sbtc-lending-integration',
                    'dimensional-vault', 'sbtc-vault', 'vault', 'liquidation-manager'
                ]
            })

        return categories

    def _load_state(self) -> Dict:
        """Load auto-detection state"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Error loading state: {e}")

        return {
            'current_directory': str(self.project_root),
            'last_scan': None,
            'contract_hashes': {},
            'deployment_status': {},
            'directory_history': [],
            'clarinet_version': self._get_clarinet_version(),
            'sdk_compatibility': '3.8'
        }

    def _get_clarinet_version(self) -> str:
        """Get Clarinet version for SDK compatibility"""
        try:
            import subprocess
            result = subprocess.run(['clarinet', '--version'],
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        return 'unknown'

    def detect_and_analyze(self) -> Dict:
        """Complete generic auto-detection and analysis"""
        print("🔍 StacksOrbit Generic Auto-Detection Starting...\n")

        # Step 1: Detect current directory and contracts
        detection_result = self._detect_current_setup()

        # Step 2: Check wallet balance if configuration is available
        wallet_status = self._check_wallet_balance()
        if wallet_status['has_balance']:
            print(f"💰 Wallet Balance: {wallet_status['balance_stx']:.6f} STX")
            if wallet_status['available_stx'] < wallet_status['recommended_minimum']:
                print(f"   ⚠️  WARNING: Low balance - add STX before deployment")
            else:
                print(f"   ✅ Sufficient balance for deployment")
        else:
            print(f"💰 Wallet: Not configured or no balance info available")

        # Step 3: Analyze deployment status
        deployment_analysis = self._analyze_deployment_status()

        # Step 4: Generate deployment plan
        deployment_plan = self._generate_generic_deployment_plan(detection_result, deployment_analysis)

        # Step 5: Save state
        self._save_state()

        return {
            'detection': detection_result,
            'deployment_analysis': deployment_analysis,
            'deployment_plan': deployment_plan,
            'wallet_status': wallet_status,
            'ready': detection_result['contracts_found'] > 0,
            'mode': 'generic' if not self.use_conxian_mode else 'conxian'
        }

    def _detect_current_setup(self) -> Dict:
        """Detect current directory setup and contracts (generic)"""
        current_dir = Path.cwd()
        print(f"📂 Current directory: {current_dir}")

        # Check if directory changed
        if str(current_dir) != self.state.get('current_directory'):
            print(f"📍 Directory change detected: {self.state.get('current_directory')} → {current_dir}")
            self.state['current_directory'] = str(current_dir)
            self.state['directory_history'].append({
                'from': self.state.get('previous_directory'),
                'to': str(current_dir),
                'timestamp': time.time()
            })
            # Clear cache for new directory
            self.contract_cache.clear()

        # Detect contracts using multiple methods (SDK 3.8 compatible)
        contracts = self._comprehensive_generic_contract_detection(current_dir)

        # Check for deployment artifacts
        deployment_artifacts = self._find_deployment_artifacts(current_dir)

        # Check for configuration (keep Conxian config support)
        config_status = self._check_configuration(current_dir)

        # Analyze Clarinet.toml for SDK compatibility
        clarinet_analysis = self._analyze_clarinet_toml(current_dir)

        return {
            'directory': str(current_dir),
            'contracts_found': len(contracts),
            'contracts': contracts,
            'deployment_artifacts': deployment_artifacts,
            'config_status': config_status,
            'clarinet_analysis': clarinet_analysis,
            'directory_changed': str(current_dir) != self.state.get('previous_directory', ''),
            'sdk_compatibility': self.state.get('sdk_compatibility', '3.8')
        }

    def _comprehensive_generic_contract_detection(self, directory: Path) -> List[Dict]:
        """Generic contract detection compatible with any Stacks project"""
        cache_key = str(directory)
        if cache_key in self.contract_cache:
            return self.contract_cache[cache_key]

        contracts = []

        # Method 1: Enhanced Clarinet.toml parsing (SDK 3.8 compatible)
        clarinet_contracts = self._parse_generic_clarinet_toml(directory)
        if clarinet_contracts:
            contracts.extend(clarinet_contracts)
            print(f"✅ Clarinet.toml detection: {len(clarinet_contracts)} contracts")

        # Method 2: Generic directory scanning (any .clar files)
        directory_contracts = self._generic_directory_scan(directory)
        if directory_contracts:
            # Avoid duplicates
            existing_names = {c['name'] for c in contracts}
            new_contracts = [c for c in directory_contracts if c['name'] not in existing_names]
            contracts.extend(new_contracts)
            print(f"✅ Directory scanning: {len(new_contracts)} additional contracts")

        # Method 3: Check for deployment manifests
        manifest_contracts = self._parse_deployment_manifests(directory)
        if manifest_contracts:
            print(f"📦 Found deployment manifests: {len(manifest_contracts)} contracts referenced")

        # Method 4: Check for standard Stacks project structures
        project_contracts = self._scan_project_structures(directory)
        if project_contracts:
            existing_names = {c['name'] for c in contracts}
            new_contracts = [c for c in project_contracts if c['name'] not in existing_names]
            contracts.extend(new_contracts)
            print(f"✅ Project structure scanning: {len(new_contracts)} additional contracts")

        # Categorize contracts generically
        contracts = self._categorize_contracts(contracts)

        # Sort by generic dependency order
        contracts = self._sort_contracts_by_generic_dependencies(contracts)

        # Cache results
        self.contract_cache[cache_key] = contracts

        return contracts

    def _parse_generic_clarinet_toml(self, directory: Path) -> List[Dict]:
        """Parse Clarinet.toml in a generic way compatible with SDK 3.8"""
        contracts = []
        clarinet_path = directory / "Clarinet.toml"

        if not clarinet_path.exists():
            return contracts

        try:
            # Try to parse as TOML first
            try:
                import tomllib
                with open(clarinet_path, 'rb') as f:
                    toml_data = tomllib.load(f)
            except ImportError:
                # Fallback for older Python versions
                try:
                    import toml
                    with open(clarinet_path, 'r') as f:
                        toml_data = toml.load(f)
                except ImportError:
                    # Manual parsing fallback
                    return self._parse_clarinet_toml_manually(clarinet_path)

            # Extract contracts from TOML structure
            if 'contracts' in toml_data:
                for contract_name, contract_config in toml_data['contracts'].items():
                    if isinstance(contract_config, dict) and 'path' in contract_config:
                        contract_path = contract_config['path']
                        full_path = directory / contract_path

                        if full_path.exists():
                            contracts.append({
                                'name': contract_name,
                                'path': contract_path,
                                'full_path': str(full_path),
                                'source': 'clarinet_toml',
                                'config': contract_config,
                                'size': full_path.stat().st_size,
                                'modified': full_path.stat().st_mtime,
                                'hash': self._calculate_file_hash(full_path),
                                'category': self._determine_contract_category(contract_name)
                            })

        except Exception as e:
            print(f"⚠️  Error parsing Clarinet.toml: {e}")
            # Fallback to manual parsing
            return self._parse_clarinet_toml_manually(clarinet_path)

        return contracts

    def _parse_clarinet_toml_manually(self, clarinet_path: Path) -> List[Dict]:
        """Manual Clarinet.toml parsing for maximum compatibility"""
        contracts = []

        try:
            with open(clarinet_path, 'r') as f:
                content = f.read()

            # Enhanced regex patterns for different Clarinet.toml formats
            patterns = [
                # SDK 3.8+ format: [contracts.name]
                r'\[contracts\.([^\]]+)\]\s+path\s*=\s*["\']([^"\']+)["\']',
                # Alternative format with dependencies
                r'\[contracts\.([^\]]+)\]\s+path\s*=\s*["\']([^"\']+)["\'].*?depends_on\s*=\s*\[(.*?)\]',
                # Simple format
                r'([^\[]+)\s*=\s*["\']([^"\']+\.clar)["\']'
            ]

            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE | re.DOTALL)
                if matches:
                    for match in matches:
                        if len(match) >= 2:
                            contract_name = match[0]
                            contract_path = match[1]

                            full_path = clarinet_path.parent / contract_path
                            if full_path.exists():
                                contracts.append({
                                    'name': contract_name,
                                    'path': contract_path,
                                    'full_path': str(full_path),
                                    'source': 'clarinet_toml',
                                    'size': full_path.stat().st_size,
                                    'modified': full_path.stat().st_mtime,
                                    'hash': self._calculate_file_hash(full_path),
                                    'category': self._determine_contract_category(contract_name)
                                })
                    break  # Use first successful pattern

        except Exception as e:
            print(f"⚠️  Manual parsing failed: {e}")

        return contracts

    def _generic_directory_scan(self, directory: Path) -> List[Dict]:
        """Generic directory scanning for any .clar files"""
        contracts = []

        # Standard Stacks project structures
        scan_patterns = [
            ("contracts/**/*.clar", "contracts directory"),
            ("clarinet/contracts/**/*.clar", "clarinet contracts"),
            ("src/**/*.clar", "src directory"),
            ("**/*.clar", "any .clar files")
        ]

        for pattern, description in scan_patterns:
            found_contracts = list(directory.glob(pattern))
            if found_contracts:
                print(f"📁 Found contracts in {description}: {len(found_contracts)} files")

                for clar_file in found_contracts:
                    if clar_file.is_file():
                        contract_name = clar_file.stem
                        contracts.append({
                            'name': contract_name,
                            'path': str(clar_file.relative_to(directory)),
                            'full_path': str(clar_file),
                            'source': description,
                            'size': clar_file.stat().st_size,
                            'modified': clar_file.stat().st_mtime,
                            'hash': self._calculate_file_hash(clar_file),
                            'category': self._determine_contract_category(contract_name)
                        })

        return contracts

    def _scan_project_structures(self, directory: Path) -> List[Dict]:
        """Scan standard Stacks project structures"""
        contracts = []

        # Check for common Stacks project structures
        structures = [
            ("clarinet", "Clarinet project structure"),
            ("contracts", "Standard contracts directory"),
            ("src/contracts", "Source contracts"),
            ("packages", "Monorepo packages"),
            ("tests/contracts", "Test contracts")
        ]

        for structure_dir, description in structures:
            structure_path = directory / structure_dir
            if structure_path.exists():
                print(f"🏗️  Found {description}: {structure_path}")

                # Look for contracts in this structure
                for clar_file in structure_path.rglob("*.clar"):
                    if clar_file.is_file():
                        contract_name = clar_file.stem
                        contracts.append({
                            'name': contract_name,
                            'path': str(clar_file.relative_to(directory)),
                            'full_path': str(clar_file),
                            'source': description,
                            'size': clar_file.stat().st_size,
                            'modified': clar_file.stat().st_mtime,
                            'hash': self._calculate_file_hash(clar_file),
                            'category': self._determine_contract_category(contract_name)
                        })

        return contracts

    def _determine_contract_category(self, contract_name: str) -> str:
        """Determine contract category generically"""
        name_lower = contract_name.lower()

        # Check against generic categories
        for category, patterns in self.contract_categories.items():
            if any(pattern in name_lower for pattern in patterns):
                return category

        # Default category
        return 'general'

    def _categorize_contracts(self, contracts: List[Dict]) -> List[Dict]:
        """Add category information to contracts"""
        if not contracts:
            return []

        for contract in contracts:
            if 'category' not in contract:
                contract['category'] = self._determine_contract_category(contract['name'])
        return contracts
    def _parse_deployment_manifests(self, directory: Path) -> List[Dict]:
        """Parse deployment manifests for contract information"""
        manifests = []

        # Check for deployment manifest files
        manifest_patterns = [
            "deployment/**/*.json",
            "**/manifest.json",
            "**/deployments.json",
            ".stacksorbit/**/*.json"
        ]

        for pattern in manifest_patterns:
            for manifest_file in directory.glob(pattern):
                if manifest_file.is_file():
                    try:
                        with open(manifest_file, 'r') as f:
                            data = json.load(f)

                        # Extract contract information if available
                        if 'deployment' in data and 'successful' in data['deployment']:
                            successful_contracts = data['deployment']['successful']
                            for contract in successful_contracts:
                                manifests.append({
                                    'name': contract.get('name', ''),
                                    'tx_id': contract.get('tx_id', ''),
                                    'source': 'deployment_manifest',
                                    'path': str(manifest_file)
                                })

                    except Exception as e:
                        print(f"⚠️  Error reading manifest {manifest_file}: {e}")

        return manifests

    def _sort_contracts_by_generic_dependencies(self, contracts: List[Dict]) -> List[Dict]:
        """Sort contracts by generic dependency order (SDK 3.8 compatible)"""
        # Generic dependency order for Stacks contracts
        priority_order = [
            # 1. Traits and interfaces (must come first)
            'trait', 'traits', 'interface', 'interfaces',
            'sip-009', 'sip-010', 'sip-013', 'sip-018',

            # 2. Utilities and libraries
            'utils', 'util', 'helper', 'library', 'lib',
            'math', 'string', 'encoding', 'crypto', 'hash',
            'error', 'constants', 'types',

            # 3. Core protocol contracts
            'core', 'main', 'principal', 'registry', 'manager',

            # 4. Token contracts
            'token', 'ft', 'nft', 'fungible', 'non-fungible',
            'mint', 'burn', 'transfer', 'balance', 'supply',

            # 5. DeFi contracts
            'dex', 'swap', 'pool', 'liquidity', 'amm', 'router', 'factory',
            'pair', 'vault', 'staking', 'farming', 'yield', 'rewards',

            # 6. Oracle contracts
            'oracle', 'price', 'feed', 'aggregator', 'adapter',

            # 7. Governance contracts
            'dao', 'governance', 'proposal', 'vote', 'voting',
            'timelock', 'upgrade', 'admin', 'owner', 'controller',

            # 8. Security and monitoring
            'auth', 'access', 'control', 'circuit', 'breaker',
            'pause', 'pausable', 'rate', 'limit', 'emergency',
            'monitor', 'analytics', 'metrics', 'dashboard',

            # 9. Testing and development
            'test', 'mock', 'fake', 'simulator', 'debug'
        ]

        # Filter out None or invalid contracts
        if not contracts:
            return []
        valid_contracts = [c for c in contracts if c and isinstance(c, dict) and c.get('name')]

        if not valid_contracts:
            return []

        def get_priority(contract):
            name = contract.get('name', '')
            if not name:
                return len(priority_order)  # Low priority for contracts without names
            name_lower = name.lower()
            for i, priority in enumerate(priority_order):
                if priority in name_lower:
                    return i
            return len(priority_order)  # Low priority for unknown contracts

        return sorted(valid_contracts, key=get_priority)

    def _analyze_clarinet_toml(self, directory: Path) -> Dict:
        """Analyze Clarinet.toml for SDK compatibility"""
        analysis = {
            'exists': False,
            'version': 'unknown',
            'compatible': True,
            'issues': [],
            'contracts': 0,
            'dependencies': []
        }

        clarinet_path = directory / "Clarinet.toml"
        if not clarinet_path.exists():
            return analysis

        analysis['exists'] = True

        try:
            # Try TOML parsing first
            try:
                import tomllib
                with open(clarinet_path, 'rb') as f:
                    toml_data = tomllib.load(f)
            except ImportError:
                try:
                    import toml
                    with open(clarinet_path, 'r') as f:
                        toml_data = toml.load(f)
                except ImportError:
                    # Manual parsing
                    return self._analyze_clarinet_toml_manually(clarinet_path)

            # Analyze project structure
            if 'project' in toml_data:
                project = toml_data['project']
                if 'name' in project:
                    analysis['project_name'] = project['name']

            # Count contracts
            if 'contracts' in toml_data:
                analysis['contracts'] = len(toml_data['contracts'])

            # Check dependencies
            if 'dependencies' in toml_data:
                analysis['dependencies'] = list(toml_data['dependencies'].keys())

            # Validate SDK 3.8 compatibility
            analysis['compatible'] = self._validate_sdk_compatibility(toml_data)
            if not analysis['compatible']:
                analysis['issues'].append('Incompatible with Clarinet SDK 3.8')

        except Exception as e:
            analysis['issues'].append(f'Parsing error: {e}')
            analysis['compatible'] = False

        return analysis

    def _validate_sdk_compatibility(self, toml_data: Dict) -> bool:
        """Validate compatibility with Clarinet SDK 3.8"""
        # Check for deprecated features
        deprecated_features = [
            'clarinet_version',  # Should use project version
            'mainnet', 'testnet'  # Should use networks
        ]

        # This is a simplified check - in reality would be more comprehensive
        return True  # Assume compatible for now

    def _analyze_clarinet_toml_manually(self, clarinet_path: Path) -> Dict:
        """Manual analysis of Clarinet.toml"""
        analysis = {
            'exists': True,
            'version': 'manual_parse',
            'compatible': True,
            'issues': [],
            'contracts': 0,
            'dependencies': []
        }

        try:
            with open(clarinet_path, 'r') as f:
                content = f.read()

            # Count contract definitions
            contract_matches = re.findall(r'\[contracts\.([^\]]+)\]', content)
            analysis['contracts'] = len(contract_matches)

            # Check for project section
            if '[project]' in content:
                analysis['has_project'] = True
            else:
                analysis['issues'].append('Missing [project] section')

        except Exception as e:
            analysis['issues'].append(f'Manual analysis error: {e}')
            analysis['compatible'] = False

    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate file hash for change detection"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return "unknown"

    def _find_deployment_artifacts(self, directory: Path) -> List[Dict]:
        """Find deployment artifacts and history"""
        artifacts = []

        # Check for various deployment-related files
        artifact_patterns = [
            "deployment/**/*.json",
            "**/manifest.json",
            "**/deployments.json",
            ".stacksorbit/**/*.json",
            "**/*.deployment"
        ]

        for pattern in artifact_patterns:
            for artifact_file in directory.glob(pattern):
                if artifact_file.is_file():
                    try:
                        with open(artifact_file, 'r') as f:
                            data = json.load(f)

                        artifacts.append({
                            'type': 'deployment_artifact',
                            'path': str(artifact_file),
                            'data': data,
                            'modified': artifact_file.stat().st_mtime
                        })
                    except Exception as e:
                        print(f"⚠️  Error reading artifact {artifact_file}: {e}")

        return artifacts

    def _check_configuration(self, directory: Path) -> Dict:
        """Check configuration status (keeping Conxian config support)"""
        config_status = {
            'has_config': False,
            'config_file': None,
            'is_valid': False,
            'missing_vars': [],
            'network': None
        }

        # Look for configuration files (including Conxian .env)
        config_files = ['.env', 'config.env', '.stacksorbit.env']

        for config_file in config_files:
            config_path = directory / config_file
            if config_path.exists():
                config_status['has_config'] = True
                config_status['config_file'] = config_file

                # Validate configuration
                is_valid, missing = self._validate_configuration(config_path)
                config_status['is_valid'] = is_valid
                config_status['missing_vars'] = missing

                # Extract network
                config_status['network'] = self._extract_network_from_config(config_path)
                break

        return config_status

    def _validate_configuration(self, config_path: Path) -> Tuple[bool, List[str]]:
        """Validate configuration file"""
        missing = []
        required_vars = ['DEPLOYER_PRIVKEY', 'SYSTEM_ADDRESS', 'NETWORK']

        try:
            with open(config_path, 'r') as f:
                config_content = {}
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        config_content[key.strip()] = value.strip()

            for var in required_vars:
                if var not in config_content or not config_content[var]:
                    missing.append(var)

            # Additional validation
            if 'DEPLOYER_PRIVKEY' in config_content:
                if len(config_content['DEPLOYER_PRIVKEY']) != 64:
                    missing.append('DEPLOYER_PRIVKEY (invalid length)')

            if 'SYSTEM_ADDRESS' in config_content:
                if not config_content['SYSTEM_ADDRESS'].startswith('S'):
                    missing.append('SYSTEM_ADDRESS (invalid format)')

        except Exception as e:
            missing.append(f'Config parsing error: {e}')

        return len(missing) == 0, missing

    def _extract_network_from_config(self, config_path: Path) -> Optional[str]:
        """Extract network from configuration"""
        try:
            with open(config_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('NETWORK='):
                        network = line.split('=', 1)[1]
                        return network
        except:
            pass
        return None

    def _analyze_deployment_status(self) -> Dict:
        """Analyze current deployment status"""
        print("📊 Analyzing deployment status...")

        # Check local deployment history
        local_status = self._check_local_deployment_status()

        # Check blockchain deployment status (if config available)
        blockchain_status = self._check_blockchain_deployment_status()

        # Compare and determine deployment mode
        deployment_mode = self._determine_deployment_mode(local_status, blockchain_status)

        return {
            'local_status': local_status,
            'blockchain_status': blockchain_status,
            'deployment_mode': deployment_mode,
            'contracts_to_skip': self._get_contracts_to_skip(local_status, blockchain_status),
            'contracts_to_deploy': self._get_contracts_to_deploy(local_status, blockchain_status)
        }

    def _check_local_deployment_status(self) -> Dict:
        """Check local deployment status from files"""
        deployment_history = []

        # Check deployment history
        history_patterns = [
            "deployment/history.json",
            ".stacksorbit/deployment_history.json",
            "**/deployment_history.json"
        ]

        for pattern in history_patterns:
            for history_file in self.project_root.glob(pattern):
                if history_file.is_file():
                    try:
                        with open(history_file, 'r') as f:
                            data = json.load(f)
                            deployment_history.extend(data)
                    except Exception as e:
                        print(f"⚠️  Error reading {history_file}: {e}")

        # Check manifest files
        manifests = []
        manifest_patterns = [
            "deployment/manifest.json",
            ".stacksorbit/manifest.json",
            "**/testnet-manifest.json",
            "**/mainnet-manifest.json"
        ]

        for pattern in manifest_patterns:
            for manifest_file in self.project_root.glob(pattern):
                if manifest_file.is_file():
                    try:
                        with open(manifest_file, 'r') as f:
                            data = json.load(f)
                            manifests.append(data)
                    except Exception as e:
                        print(f"⚠️  Error reading {manifest_file}: {e}")

        return {
            'has_local_history': len(deployment_history) > 0,
            'deployment_history': deployment_history,
            'manifests': manifests,
            'last_deployment': deployment_history[-1] if deployment_history else None
        }

    def _check_blockchain_deployment_status(self) -> Dict:
        """Check blockchain deployment status"""
        # This would require API access and valid configuration
        # For now, return mock data based on local state

        config_path = self.project_root / ".env"
        if not config_path.exists():
            return {'status': 'no_config', 'error': 'No configuration file found'}

        network = self._extract_network_from_config(config_path)
        if not network:
            return {'status': 'no_network', 'error': 'No network specified in config'}

        # In a real implementation, this would query the Hiro API
        # For now, simulate based on local state
        return {
            'status': 'simulated',
            'network': network,
            'account_nonce': 0,  # Would query API
            'deployed_contracts': [],  # Would query API
            'last_activity': None
        }

    def _determine_deployment_mode(self, local_status: Dict, blockchain_status: Dict) -> str:
        """Determine deployment mode based on status"""
        if blockchain_status.get('account_nonce', 0) > 0:
            return 'upgrade'
        elif local_status.get('has_local_history', False):
            return 'incremental'
        else:
            return 'full'

    def _get_contracts_to_skip(self, local_status: Dict, blockchain_status: Dict) -> List[str]:
        """Get contracts that should be skipped (already deployed)"""
        skip_contracts = set()

        # Add contracts from blockchain status
        if blockchain_status.get('deployed_contracts'):
            skip_contracts.update(blockchain_status['deployed_contracts'])

        # Add contracts from local manifests
        for manifest in local_status.get('manifests', []):
            successful = manifest.get('deployment', {}).get('successful', [])
            for contract in successful:
                skip_contracts.add(contract.get('name'))

        return list(skip_contracts)

    def _get_contracts_to_deploy(self, local_status: Dict, blockchain_status: Dict) -> List[str]:
        """Get contracts that need to be deployed"""
        # Get all available contracts
        all_contracts = self.contract_cache.get(str(self.project_root), [])
        all_contract_names = {c['name'] for c in all_contracts}

        # Remove contracts that should be skipped
        skip_contracts = set(self._get_contracts_to_skip(local_status, blockchain_status))
        deploy_contracts = all_contract_names - skip_contracts

        return list(deploy_contracts)

    def _generate_generic_deployment_plan(self, detection: Dict, deployment_analysis: Dict) -> Dict:
        """Generate comprehensive deployment plan"""
        contracts = detection['contracts']
        deployment_mode = deployment_analysis['deployment_mode']
        contracts_to_skip = deployment_analysis['contracts_to_skip']
        contracts_to_deploy = deployment_analysis['contracts_to_deploy']

        # Filter contracts based on deployment mode
        if deployment_mode == 'upgrade':
            filtered_contracts = [c for c in contracts if c['name'] not in contracts_to_skip]
        else:
            filtered_contracts = contracts

        # Sort by generic dependency order
        filtered_contracts = self._sort_contracts_by_generic_dependencies(filtered_contracts)

        # Calculate deployment metrics
        total_contracts = len(contracts)
        skipped_contracts = len(contracts_to_skip)
        to_deploy = len(contracts_to_deploy)

        return {
            'deployment_mode': deployment_mode,
            'total_contracts': total_contracts,
            'contracts_to_deploy': to_deploy,
            'contracts_to_skip': skipped_contracts,
            'filtered_contracts': filtered_contracts,
            'estimated_gas': self._estimate_total_gas(filtered_contracts),
            'estimated_time': self._estimate_deployment_time(filtered_contracts),
            'deployment_order': [c['name'] for c in filtered_contracts]
        }

    def _estimate_total_gas(self, contracts: List[Dict]) -> float:
        """Estimate total gas for deployment"""
        total_gas = 0
        for contract in contracts:
            # Base gas per contract (generic estimation)
            base_gas = 1.0
            # Complexity multipliers based on category
            category = contract.get('category', 'general')
            if category in ['defi', 'dao']:
                base_gas *= 1.8
            elif category in ['tokens', 'oracle']:
                base_gas *= 1.3
            elif category in ['security', 'utilities']:
                base_gas *= 1.1

            total_gas += base_gas

        return total_gas

    def _estimate_deployment_time(self, contracts: List[Dict]) -> int:
        """Estimate deployment time in minutes"""
        # Base time per contract (including confirmations)
        base_time_per_contract = 2  # minutes
        total_time = len(contracts) * base_time_per_contract

        # Add buffer for complex contracts
        complex_contracts = [c for c in contracts if c.get('category') in ['defi', 'dao']]
        total_time += len(complex_contracts) * 1  # Extra minute for complex contracts

        return max(total_time, 5)  # Minimum 5 minutes

    def _save_state(self):
        """Save auto-detection state"""
        self.state['last_updated'] = time.time()

        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)

    def handle_directory_change(self, new_directory: Path) -> Dict:
        """Handle directory change and update detection"""
        print(f"\n📂 Handling directory change to: {new_directory}")

        old_dir = self.state.get('current_directory', '')
        self.state['previous_directory'] = old_dir
        self.state['current_directory'] = str(new_directory)

        # Clear caches for new directory
        self.contract_cache.clear()
        self.deployment_cache.clear()

        # Re-run detection in new directory
        result = self.detect_and_analyze()

        # Record the change
        self.state['directory_history'].append({
            'from': old_dir,
            'to': str(new_directory),
            'timestamp': time.time(),
            'contracts_found': result['detection']['contracts_found']
        })

        self._save_state()

        return result

    def get_deployment_recommendations(self, analysis: Dict) -> List[str]:
        """Get deployment recommendations based on analysis"""
        recommendations = []

        detection = analysis['detection']
        deployment_analysis = analysis['deployment_analysis']
        deployment_plan = analysis['deployment_plan']

        # Configuration recommendations
        if not detection['config_status']['has_config']:
            recommendations.append("❌ No configuration file found. Run 'python setup_wizard.py' to create one.")
        elif not detection['config_status']['is_valid']:
            missing = detection['config_status']['missing_vars']
            recommendations.append(f"❌ Configuration invalid. Missing: {', '.join(missing)}")

        # Contract recommendations
        if detection['contracts_found'] == 0:
            recommendations.append("❌ No contracts found. Check directory structure or create Clarinet.toml.")
        elif deployment_plan['contracts_to_deploy'] == 0:
            recommendations.append("✅ All contracts already deployed. Use --force to redeploy.")

        # Clarinet SDK compatibility
        clarinet_analysis = detection.get('clarinet_analysis', {})
        if not clarinet_analysis.get('compatible', True):
            recommendations.append("⚠️  Clarinet.toml may not be compatible with SDK 3.8")
            for issue in clarinet_analysis.get('issues', []):
                recommendations.append(f"   - {issue}")

        # Deployment mode recommendations
        mode = deployment_plan['deployment_mode']
        if mode == 'upgrade':
            recommendations.append("🔄 Upgrade mode: Only new/changed contracts will be deployed.")
        elif mode == 'full':
            recommendations.append("🆕 Full deployment mode: All contracts will be deployed.")

        # Gas and time estimates
        if deployment_plan['estimated_gas'] > 50:
            recommendations.append(f"⚠️  High gas usage estimated: {deployment_plan['estimated_gas']:.1f} STX")

        if deployment_plan['estimated_time'] > 30:
            recommendations.append(f"⏰ Long deployment estimated: {deployment_plan['estimated_time']} minutes")

        return recommendations

    def _check_wallet_balance(self) -> Dict:
        """Check wallet balance and deployment readiness"""
        wallet_status = {
            'has_balance': False,
            'balance_stx': 0.0,
            'available_stx': 0.0,
            'locked_stx': 0.0,
            'recommended_minimum': 5.0,  # Minimum recommended for deployment
            'network': None,
            'address': None
        }

        # Check configuration
        config_status = self._check_configuration(self.project_root)
        if not config_status['is_valid']:
            return wallet_status

        # Get address from config
        address = self._extract_address_from_config()
        network = config_status.get('network')

        if not address or not network:
            return wallet_status

        wallet_status['address'] = address
        wallet_status['network'] = network

        try:
            # Try to get account info using requests (simplified)
            import requests

            api_urls = {
                'mainnet': 'https://api.hiro.so',
                'testnet': 'https://api.testnet.hiro.so',
                'devnet': 'http://localhost:20443'
            }

            api_url = api_urls.get(network, api_urls['testnet'])

            response = requests.get(f"{api_url}/v2/accounts/{address}", timeout=10)
            if response.status_code == 200:
                data = response.json()

                balance_microstx = int(data.get('balance', 0))
                locked_microstx = int(data.get('locked', 0))

                balance_stx = balance_microstx / 1000000
                locked_stx = locked_microstx / 1000000
                available_stx = balance_stx - locked_stx

                wallet_status.update({
                    'has_balance': True,
                    'balance_stx': balance_stx,
                    'available_stx': available_stx,
                    'locked_stx': locked_stx
                })

        except Exception as e:
            print(f"⚠️  Could not check wallet balance: {e}")

        return wallet_status

    def _extract_address_from_config(self) -> Optional[str]:
        """Extract Stacks address from configuration"""
        config_files = ['.env', 'config.env', '.stacksorbit.env']

        for config_file in config_files:
            config_path = self.project_root / config_file
            if config_path.exists():
                try:
                    with open(config_path, 'r') as f:
                        for line in f:
                            line = line.strip()
                            if line.startswith('SYSTEM_ADDRESS='):
                                address = line.split('=', 1)[1].strip().strip('"')
                                if address.startswith('S') and len(address) == 41:
                                    return address
                except:
                    continue

        return None

def main():
    """Main auto-detection function"""
    print("🚀 StacksOrbit Generic Auto-Detection System")
    print("=" * 55)

    # Check if Conxian mode is requested via environment
    use_conxian = os.getenv('STACKSORBIT_CONXIAN_MODE', 'false').lower() == 'true'

    # Initialize detector
    detector = GenericStacksAutoDetector(use_conxian_mode=use_conxian)

    # Run complete detection and analysis
    analysis = detector.detect_and_analyze()

    # Show results
    print(f"\n📂 Directory: {analysis['detection']['directory']}")
    print(f"📦 Contracts found: {analysis['detection']['contracts_found']}")
    print(f"📊 Deployment mode: {analysis['deployment_plan']['deployment_mode']}")
    print(f"🚀 Contracts to deploy: {analysis['deployment_plan']['contracts_to_deploy']}")
    print(f"⏭️  Contracts to skip: {analysis['deployment_plan']['contracts_to_skip']}")
    print(f"🏷️  Mode: {analysis['mode']}")

    # Show SDK compatibility
    sdk_compat = analysis['detection']['sdk_compatibility']
    print(f"🔧 SDK Compatibility: {sdk_compat}")

    # Show recommendations
    recommendations = detector.get_deployment_recommendations(analysis)
    if recommendations:
        print("\n💡 Recommendations:")
        for rec in recommendations:
            print(f"   {rec}")

    # Show deployment plan
    if analysis['deployment_plan']['filtered_contracts']:
        print("\n📋 Deployment order:")
        for i, contract in enumerate(analysis['deployment_plan']['filtered_contracts'][:10], 1):
            category = contract.get('category', 'general')
            print(f"   {i}. {contract['name']} ({category})")

        if len(analysis['deployment_plan']['filtered_contracts']) > 10:
            print(f"   ... and {len(analysis['deployment_plan']['filtered_contracts']) - 10} more")

    print(f"\n⛽ Estimated gas: {analysis['deployment_plan']['estimated_gas']:.1f} STX")
    print(f"⏰ Estimated time: {analysis['deployment_plan']['estimated_time']} minutes")

    print(f"\n✅ Ready: {analysis['ready']}")

    return 0 if analysis['ready'] else 1

if __name__ == "__main__":
    exit(main())
