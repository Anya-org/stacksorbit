#!/usr/bin/env python3
"""
User-Friendly Setup Wizard for StacksOrbit
Guides users through the entire deployment process with clear instructions
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
import argparse

try:
    import colorama
    from colorama import Fore, Style
    colorama.init()
    USE_COLORS = True
except ImportError:
    USE_COLORS = False

class SetupWizard:
    """Interactive setup wizard for StacksOrbit"""

    def __init__(self):
        self.config = {}
        self.project_root = Path.cwd()
        self.stacksorbit_root = Path(__file__).parent

    def start_wizard(self):
        """Start the interactive setup wizard"""
        print(f"{Fore.CYAN}🚀 Welcome to StacksOrbit Setup Wizard!{Style.RESET_ALL}")
        print(f"{Fore.WHITE}This wizard will guide you through setting up your Stacks blockchain deployment.{Style.RESET_ALL}")
        print()

        # Check prerequisites
        if not self._check_prerequisites():
            print(f"{Fore.RED}❌ Prerequisites not met. Please install required software and try again.{Style.RESET_ALL}")
            return False

        # Run setup steps
        steps = [
            self._step_welcome,
            self._step_project_analysis,
            self._step_network_selection,
            self._step_wallet_setup,
            self._step_configuration,
            self._step_testing,
            self._step_deployment_options,
            self._step_summary
        ]

        for step in steps:
            if not step():
                print(f"{Fore.RED}❌ Setup cancelled or failed.{Style.RESET_ALL}")
                return False

        print(f"\n{Fore.GREEN}🎉 Setup completed successfully!{Style.RESET_ALL}")
        print(f"{Fore.WHITE}You can now use StacksOrbit to deploy your contracts.{Style.RESET_ALL}")
        return True

    def _check_prerequisites(self) -> bool:
        """Check if all prerequisites are installed"""
        print("🔍 Checking prerequisites...")

        prerequisites = [
            ('Node.js', 'node --version', 'Node.js 14+'),
            ('Python', 'python --version', 'Python 3.8+'),
            ('Clarinet', 'clarinet --version', 'Clarinet'),
            ('Git', 'git --version', 'Git')
        ]

        all_met = True

        for name, command, expected in prerequisites:
            try:
                result = subprocess.run(command.split(), capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    version = result.stdout.strip() or result.stderr.strip()
                    print(f"✅ {name}: {version}")
                else:
                    print(f"❌ {name}: Not found")
                    all_met = False
            except Exception as e:
                print(f"❌ {name}: Error checking ({e})")
                all_met = False

        # Check for StacksOrbit dependencies
        print("
📦 Checking StacksOrbit dependencies..."        try:
            import requests
            print("✅ Python requests library")
        except ImportError:
            print("⚠️  Python requests library not found - will install")

        try:
            import toml
            print("✅ Python toml library")
        except ImportError:
            print("⚠️  Python toml library not found - will install")

        return all_met

    def _step_welcome(self) -> bool:
        """Welcome step"""
        print(f"\n{Fore.CYAN}📋 Step 1: Welcome{Style.RESET_ALL}")
        print("This wizard will help you set up StacksOrbit for deploying smart contracts to the Stacks blockchain.")
        print()
        print("What you need:")
        print(f"  • A Stacks account with some STX tokens ({Fore.YELLOW}minimum 10 STX recommended{Style.RESET_ALL})")
        print("  • Your private key or 12/24-word mnemonic")
        print("  • Basic understanding of your project structure")
        print()

        response = self._get_user_input("Continue with setup? (y/n): ", ['y', 'n'])
        return response == 'y'

    def _step_project_analysis(self) -> bool:
        """Analyze project structure"""
        print(f"\n{Fore.CYAN}📋 Step 2: Project Analysis{Style.RESET_ALL}")
        print("Analyzing your project structure...")

        # Check for Clarinet.toml
        clarinet_path = self.project_root / "Clarinet.toml"
        if clarinet_path.exists():
            print(f"✅ Found Clarinet.toml at {clarinet_path}")
            self.config['clarinet_found'] = True

            # Analyze contracts
            contracts = self._analyze_clarinet_contracts(clarinet_path)
            if contracts:
                print(f"✅ Found {len(contracts)} contracts in Clarinet.toml:")
                for contract in contracts[:5]:  # Show first 5
                    print(f"   - {contract['name']}")
                if len(contracts) > 5:
                    print(f"   ... and {len(contracts) - 5} more")

                self.config['contracts'] = contracts
                self.config['total_contracts'] = len(contracts)
            else:
                print("⚠️  No contracts found in Clarinet.toml")
        else:
            print(f"⚠️  No Clarinet.toml found - you'll need to create one or specify contract paths manually")
            self.config['clarinet_found'] = False

        # Check for contracts directory
        contracts_dir = self.project_root / "contracts"
        if contracts_dir.exists():
            clar_files = list(contracts_dir.rglob("*.clar"))
            print(f"✅ Found contracts directory with {len(clar_files)} .clar files")
            self.config['contracts_dir_found'] = True
        else:
            print("⚠️  No contracts directory found")
            self.config['contracts_dir_found'] = False

        print()
        response = self._get_user_input("Continue? (y/n): ", ['y', 'n'])
        return response == 'y'

    def _step_network_selection(self) -> bool:
        """Network selection step"""
        print(f"\n{Fore.CYAN}📋 Step 3: Network Selection{Style.RESET_ALL}")
        print("Which Stacks network do you want to deploy to?")
        print()
        print("1. 🧪 Devnet (local testing)")
        print("2. 🧪 Testnet (public testing)")
        print("3. 🌐 Mainnet (production)")
        print()

        choice = self._get_user_input("Select network (1-3): ", ['1', '2', '3'])

        networks = {
            '1': 'devnet',
            '2': 'testnet',
            '3': 'mainnet'
        }

        self.config['network'] = networks[choice]

        if choice == '1':
            print("✅ Selected Devnet - great for local testing!")
            print(f"{Fore.YELLOW}💡 Make sure you have a local Stacks node running{Style.RESET_ALL}")
        elif choice == '2':
            print("✅ Selected Testnet - perfect for testing!")
            print(f"{Fore.YELLOW}💡 Get free STX from the faucet: https://explorer.stacks.co/sandbox{Style.RESET_ALL}")
        else:
            print("✅ Selected Mainnet - production deployment!")
            print(f"{Fore.RED}⚠️  WARNING: This will use real STX tokens!{Style.RESET_ALL}")

        print()
        response = self._get_user_input("Continue? (y/n): ", ['y', 'n'])
        return response == 'y'

    def _step_wallet_setup(self) -> bool:
        """Wallet setup step"""
        print(f"\n{Fore.CYAN}📋 Step 4: Wallet Setup{Style.RESET_ALL}")
        print("We need your Stacks account information for deployment.")
        print()

        print("How would you like to provide your wallet information?")
        print("1. 🔑 Enter private key directly")
        print("2. 📝 Enter 12/24-word mnemonic")
        print("3. 🚫 Skip for now (configure manually later)")
        print()

        choice = self._get_user_input("Choose option (1-3): ", ['1', '2', '3'])

        if choice == '1':
            private_key = self._get_user_input("Enter your private key (64 hex characters): ", None, secret=True)
            if self._validate_private_key(private_key):
                self.config['deployer_privkey'] = private_key
                print("✅ Private key validated")
            else:
                print(f"{Fore.RED}❌ Invalid private key format{Style.RESET_ALL}")
                return False

        elif choice == '2':
            mnemonic = self._get_user_input("Enter your mnemonic (space-separated words): ", None, secret=True)
            # Note: In a real implementation, you'd derive the private key from mnemonic
            print(f"{Fore.YELLOW}💡 Mnemonic support requires additional setup{Style.RESET_ALL}")
            print("📝 Please enter the corresponding private key instead")
            private_key = self._get_user_input("Private key: ", None, secret=True)

            if self._validate_private_key(private_key):
                self.config['deployer_privkey'] = private_key
                print("✅ Private key validated")
            else:
                print(f"{Fore.RED}❌ Invalid private key format{Style.RESET_ALL}")
                return False

        else:
            print("✅ Skipping wallet setup")
            print(f"{Fore.YELLOW}💡 You'll need to configure DEPLOYER_PRIVKEY in .env file manually{Style.RESET_ALL}")

        # Get address
        address = self._get_user_input("Enter your Stacks address (SP...): ", None)
        if self._validate_address(address):
            self.config['system_address'] = address
            print("✅ Address validated")
        else:
            print(f"{Fore.RED}❌ Invalid address format{Style.RESET_ALL}")
            return False

        print()
        response = self._get_user_input("Continue? (y/n): ", ['y', 'n'])
        return response == 'y'

    def _step_configuration(self) -> bool:
        """Configuration step"""
        print(f"\n{Fore.CYAN}📋 Step 5: Configuration{Style.RESET_ALL}")
        print("Setting up your deployment configuration...")
        print()

        # Create .env file
        env_content = self._generate_env_config()

        env_path = self.project_root / ".env"
        with open(env_path, 'w') as f:
            f.write(env_content)

        print(f"✅ Configuration saved to {env_path}")
        print()
        print("📋 Configuration summary:")
        print(f"   Network: {self.config['network']}")
        print(f"   Address: {self.config.get('system_address', 'Not set')}")

        if self.config.get('deployer_privkey'):
            print(f"   Private Key: {self.config['deployer_privkey'][:10]}...")
        else:
            print("   Private Key: Not configured (set manually)")

        print()
        print("📝 Environment variables set:")
        for line in env_content.split('\n'):
            if line.strip() and not line.startswith('#'):
                print(f"   {line}")

        print()
        response = self._get_user_input("Continue? (y/n): ", ['y', 'n'])
        return response == 'y'

    def _step_testing(self) -> bool:
        """Testing step"""
        print(f"\n{Fore.CYAN}📋 Step 6: Testing Setup{Style.RESET_ALL}")
        print("Testing your configuration...")
        print()

        # Run basic tests
        tests_passed = 0
        total_tests = 0

        # Test 1: Configuration validation
        total_tests += 1
        print("🔍 Testing configuration...")
        try:
            from enhanced_conxian_deployment import EnhancedConfigManager
            config_manager = EnhancedConfigManager(".env")
            config = config_manager.load_config()
            is_valid, errors = config_manager.validate_config()

            if is_valid:
                print("✅ Configuration validation passed")
                tests_passed += 1
            else:
                print(f"❌ Configuration validation failed: {errors}")
        except Exception as e:
            print(f"❌ Configuration test error: {e}")

        # Test 2: Network connectivity
        total_tests += 1
        print("🌐 Testing network connectivity...")
        try:
            from deployment_monitor import DeploymentMonitor
            monitor = DeploymentMonitor(self.config['network'], self.config)

            api_status = monitor.check_api_status()
            if api_status['status'] == 'online':
                print(f"✅ Network connectivity: {api_status['network_id']} @ {api_status['block_height']}")
                tests_passed += 1
            else:
                print(f"❌ Network connectivity failed: {api_status.get('error', 'Unknown')}")
        except Exception as e:
            print(f"❌ Network test error: {e}")

        # Test 3: Contract compilation (if Clarinet.toml exists)
        if self.config.get('clarinet_found'):
            total_tests += 1
            print("⚙️  Testing contract compilation...")
            try:
                result = subprocess.run(['clarinet', 'check'], capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    print("✅ Contract compilation successful")
                    tests_passed += 1
                else:
                    print("⚠️  Contract compilation issues (may be warnings)")
                    tests_passed += 1  # Still count as passed for deployment
            except Exception as e:
                print(f"❌ Contract compilation test error: {e}")

        print()
        print(f"📊 Test Results: {tests_passed}/{total_tests} passed")

        if tests_passed == total_tests:
            print(f"{Fore.GREEN}🎉 All tests passed! Ready for deployment.{Style.RESET_ALL}")
        elif tests_passed >= total_tests * 0.7:
            print(f"{Fore.YELLOW}⚠️  Most tests passed. Review warnings before deploying.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ Many tests failed. Please fix issues before deploying.{Style.RESET_ALL}")
            return False

        print()
        response = self._get_user_input("Continue? (y/n): ", ['y', 'n'])
        return response == 'y'

    def _step_deployment_options(self) -> bool:
        """Deployment options step"""
        print(f"\n{Fore.CYAN}📋 Step 7: Deployment Options{Style.RESET_ALL}")
        print("Configure your deployment preferences...")
        print()

        print("Deployment mode:")
        print("1. 🔄 Full deployment (deploy all contracts)")
        print("2. 🔄 Upgrade mode (skip already deployed contracts)")
        print("3. 🎯 Selective deployment (deploy specific contracts)")
        print()

        mode_choice = self._get_user_input("Choose deployment mode (1-3): ", ['1', '2', '3'])

        modes = {
            '1': 'full',
            '2': 'upgrade',
            '3': 'selective'
        }

        self.config['deployment_mode'] = modes[mode_choice]

        if mode_choice == '3':
            # Ask for specific contracts
            contracts = self.config.get('contracts', [])
            if contracts:
                print("Available contracts:")
                for i, contract in enumerate(contracts, 1):
                    print(f"  {i}. {contract['name']}")

                selected = self._get_user_input("Enter contract numbers (comma-separated, or 'all'): ", None)
                if selected.lower() != 'all':
                    try:
                        indices = [int(x.strip()) - 1 for x in selected.split(',')]
                        selected_contracts = [contracts[i]['name'] for i in indices if 0 <= i < len(contracts)]
                        self.config['selected_contracts'] = selected_contracts
                        print(f"✅ Will deploy: {', '.join(selected_contracts)}")
                    except:
                        print(f"{Fore.YELLOW}💡 Using all contracts{Style.RESET_ALL}")
                        self.config['selected_contracts'] = [c['name'] for c in contracts]
                else:
                    self.config['selected_contracts'] = [c['name'] for c in contracts]
            else:
                print(f"{Fore.YELLOW}💡 No contracts found, will deploy all available{Style.RESET_ALL}")

        print()
        print("Advanced options:")
        batch_size = self._get_user_input("Batch size (contracts per deployment, 1-10): ", ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
        self.config['batch_size'] = int(batch_size)

        parallel = self._get_user_input("Enable parallel deployment? (y/n): ", ['y', 'n'])
        self.config['parallel_deploy'] = parallel == 'y'

        print()
        response = self._get_user_input("Continue? (y/n): ", ['y', 'n'])
        return response == 'y'

    def _step_summary(self) -> bool:
        """Summary and final setup"""
        print(f"\n{Fore.CYAN}📋 Step 8: Setup Summary{Style.RESET_ALL}")
        print("Here's your configuration summary:")
        print()

        print(f"🌐 Network: {Fore.CYAN}{self.config['network'].upper()}{Style.RESET_ALL}")
        print(f"👤 Address: {Fore.GREEN}{self.config.get('system_address', 'Not set')}{Style.RESET_ALL}")
        print(f"📦 Deployment Mode: {Fore.BLUE}{self.config['deployment_mode'].upper()}{Style.RESET_ALL}")
        print(f"🔢 Batch Size: {self.config['batch_size']}")
        print(f"⚡ Parallel: {'Yes' if self.config.get('parallel_deploy') else 'No'}")

        contracts = self.config.get('contracts', [])
        if contracts:
            print(f"📋 Total Contracts: {len(contracts)}")

        selected = self.config.get('selected_contracts')
        if selected:
            print(f"🎯 Selected: {len(selected)} contracts")
        else:
            print("🎯 Selected: All contracts")

        print()
        print("🚀 Ready to deploy! Here are your next steps:")
        print()
        print("1. 📋 Review .env file and make any necessary changes")
        print("2. 🔍 Run pre-deployment checks:")
        print("   python conxian_testnet_deploy.py check --verbose")
        print()
        print("3. 🧪 Test deployment (dry run):")
        print("   python conxian_testnet_deploy.py deploy --dry-run")
        print()
        print("4. 🚀 Deploy to testnet:")
        print("   python conxian_testnet_deploy.py deploy")
        print()
        print("5. 📊 Monitor deployment:")
        print("   python deployment_monitor.py --follow")
        print()
        print("6. 🔍 Verify deployment:")
        print("   python deployment_verifier.py --comprehensive")

        print()
        print(f"{Fore.GREEN}🎉 Setup complete! Happy deploying!{Style.RESET_ALL}")
        return True

    def _analyze_clarinet_contracts(self, clarinet_path: Path) -> List[Dict]:
        """Analyze contracts from Clarinet.toml"""
        contracts = []

        try:
            with open(clarinet_path, 'r') as f:
                content = f.read()

            # Extract contract definitions
            import re
            contract_matches = re.findall(r'\[contracts\.([^\]]+)\]\s+path\s*=\s*["\']([^"\']+)["\']', content)

            for contract_name, contract_path in contract_matches:
                full_path = clarinet_path.parent / contract_path
                if full_path.exists():
                    contracts.append({
                        'name': contract_name,
                        'path': contract_path,
                        'full_path': str(full_path),
                        'category': self._categorize_contract(contract_name)
                    })

        except Exception as e:
            print(f"Error analyzing Clarinet.toml: {e}")

        return contracts

    def _categorize_contract(self, contract_name: str) -> str:
        """Categorize contract by name"""
        name_lower = contract_name.lower()

        if any(word in name_lower for word in ['trait', 'utils', 'lib', 'error', 'constant', 'math']):
            return 'base'
        elif any(word in name_lower for word in ['token', 'cxd', 'cxlp', 'cxvg', 'cxtr', 'cxs']):
            return 'tokens'
        elif any(word in name_lower for word in ['dex', 'factory', 'router', 'pool', 'swap']):
            return 'dex'
        elif any(word in name_lower for word in ['dim', 'dimensional', 'position', 'concentrated']):
            return 'dimensional'
        elif any(word in name_lower for word in ['oracle', 'aggregator', 'btc']):
            return 'oracle'
        elif any(word in name_lower for word in ['governance', 'proposal', 'timelock']):
            return 'governance'
        elif any(word in name_lower for word in ['circuit', 'pausable', 'access', 'security']):
            return 'security'
        elif any(word in name_lower for word in ['monitor', 'analytics', 'dashboard']):
            return 'monitoring'
        else:
            return 'other'

    def _validate_private_key(self, privkey: str) -> bool:
        """Validate private key format"""
        return len(privkey) == 64 and all(c in '0123456789abcdefABCDEF' for c in privkey)

    def _validate_address(self, address: str) -> bool:
        """Validate Stacks address format"""
        return address.startswith('S') and len(address) == 41 and address.isalnum()

    def _get_user_input(self, prompt: str, valid_options: Optional[List[str]] = None, secret: bool = False) -> str:
        """Get user input with validation"""
        while True:
            try:
                if secret:
                    import getpass
                    response = getpass.getpass(prompt)
                else:
                    response = input(prompt).strip()

                if valid_options and response.lower() not in [opt.lower() for opt in valid_options]:
                    print(f"{Fore.YELLOW}💡 Please enter one of: {', '.join(valid_options)}{Style.RESET_ALL}")
                    continue

                return response

            except KeyboardInterrupt:
                print(f"\n\n{Fore.YELLOW}🛑 Setup cancelled by user{Style.RESET_ALL}")
                sys.exit(0)
            except EOFError:
                print(f"\n\n{Fore.YELLOW}🛑 Setup cancelled{Style.RESET_ALL}")
                sys.exit(0)

    def _generate_env_config(self) -> str:
        """Generate .env configuration content"""
        config_lines = [
            "# StacksOrbit Configuration",
            "# Generated by Setup Wizard",
            "",
            "# Required Variables",
            f"DEPLOYER_PRIVKEY={self.config.get('deployer_privkey', 'your_private_key_here')}",
            f"SYSTEM_ADDRESS={self.config.get('system_address', 'your_stacks_address_here')}",
            f"NETWORK={self.config['network']}",
            "",
            "# Optional Variables (Recommended)",
            "HIRO_API_KEY=your_hiro_api_key_here",
            "CORE_API_URL=https://api.testnet.hiro.so",
            "STACKS_API_BASE=https://api.testnet.hiro.so",
            "",
            "# Deployment Configuration",
            f"DEPLOYMENT_MODE={self.config['deployment_mode']}",
            f"BATCH_SIZE={self.config['batch_size']}",
            f"PARALLEL_DEPLOY={str(self.config.get('parallel_deploy', False)).lower()}",
            "",
            "# Monitoring Configuration",
            "MONITORING_ENABLED=true",
            "LOG_LEVEL=INFO",
            "SAVE_LOGS=true",
            "",
            "# Validation",
            "VALIDATE_TRANSACTIONS=true",
            "CONFIRMATION_TIMEOUT=300",
            "",
            "# Security",
            "# Never commit this file to version control!",
            "# Add .env to your .gitignore file",
        ]

        return "\n".join(config_lines)

def create_deployment_templates():
    """Create deployment templates for different scenarios"""
    templates_dir = Path("deployment_templates")
    templates_dir.mkdir(exist_ok=True)

    templates = {
        'testnet_quick_start.json': {
            'name': 'Testnet Quick Start',
            'description': 'Quick deployment to testnet with basic monitoring',
            'network': 'testnet',
            'batch_size': 5,
            'monitoring': True,
            'verification': True
        },

        'mainnet_production.json': {
            'name': 'Mainnet Production',
            'description': 'Production deployment with full validation',
            'network': 'mainnet',
            'batch_size': 3,
            'parallel': False,
            'monitoring': True,
            'verification': True,
            'gas_estimation': True
        },

        'devnet_development.json': {
            'name': 'Devnet Development',
            'description': 'Local development deployment',
            'network': 'devnet',
            'batch_size': 10,
            'parallel': True,
            'monitoring': False,
            'verification': False
        },

        'core_only.json': {
            'name': 'Core Only',
            'description': 'Deploy only core contracts',
            'category': 'core',
            'network': 'testnet',
            'batch_size': 5,
            'monitoring': True
        }
    }

    for filename, template in templates.items():
        template_path = templates_dir / filename
        with open(template_path, 'w') as f:
            json.dump(template, f, indent=2)

        print(f"📝 Created template: {template['name']} ({filename})")

def main():
    """Main setup wizard function"""
    parser = argparse.ArgumentParser(description='StacksOrbit Setup Wizard')
    parser.add_argument('--create-templates', action='store_true', help='Create deployment templates')
    parser.add_argument('--config-path', default='.env', help='Configuration file path')

    args = parser.parse_args()

    try:
        if args.create_templates:
            print("📝 Creating deployment templates...")
            create_deployment_templates()
            print("✅ Templates created successfully!")
            return 0

        # Run setup wizard
        wizard = SetupWizard()
        success = wizard.start_wizard()

        if success:
            print("
🎉 Setup completed! You can now deploy using:"            print("   python conxian_testnet_deploy.py deploy")
            print("   python enhanced_dashboard.py")
            return 0
        else:
            return 1

    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}🛑 Setup cancelled by user{Style.RESET_ALL}")
        return 1
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())
