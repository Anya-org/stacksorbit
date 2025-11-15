#!/usr/bin/env python3
"""
Ultimate StacksOrbit Integration Script
One-stop solution for deploying to Stacks blockchain with enhanced features
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# Import all enhanced modules
from setup_wizard import SetupWizard
from enhanced_conxian_deployment import EnhancedConfigManager, EnhancedConxianDeployer
from deployment_monitor import DeploymentMonitor
from deployment_verifier import DeploymentVerifier
from enhanced_dashboard import EnhancedDashboard
from local_devnet import LocalDevnet

class UltimateStacksOrbit:
    """Ultimate deployment solution for Stacks blockchain"""

    def __init__(self):
        self.project_root = Path.cwd()
        self.config_path = ".env"
        self.templates_path = "deployment_templates.json"

        # Load deployment templates
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict:
        """Load deployment templates"""
        template_file = Path(__file__).parent / self.templates_path
        if template_file.exists():
            with open(template_file, 'r') as f:
                return json.load(f)
        return {}

    def run_command(self, command: str, **kwargs) -> int:
        """Run StacksOrbit command with enhanced features"""
        print(f"\n{Fore.CYAN}🚀 Executing: {command}{Style.RESET_ALL}")

        try:
            if command == 'setup':
                return self.run_setup_wizard()
            elif command == 'deploy':
                return self.run_enhanced_deployment(kwargs)
            elif command == 'monitor':
                return self.run_enhanced_monitoring(kwargs)
            elif command == 'verify':
                return self.run_enhanced_verification(kwargs)
            elif command == 'dashboard':
                return self.run_enhanced_dashboard(kwargs)
            elif command == 'diagnose':
                return self.run_comprehensive_diagnosis(kwargs)
            elif command == 'template':
                return self.apply_deployment_template(kwargs)
            elif command == 'devnet':
                return self.run_devnet(kwargs)
            else:
                self.show_help()
                return 1

        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}🛑 Operation cancelled by user{Style.RESET_ALL}")
            return 1
        except Exception as e:
            print(f"\n{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
            if kwargs.get('verbose'):
                import traceback
                traceback.print_exc()
            return 1

    def run_setup_wizard(self) -> int:
        """Run enhanced setup wizard"""
        wizard = SetupWizard()
        success = wizard.start_wizard()

        if success:
            print(f"\n{Fore.GREEN}✅ Setup completed!{Style.RESET_ALL}")
            print("💡 Next: Run 'stacksorbit deploy --dry-run' to test deployment")
        return 0 if success else 1

    def run_enhanced_deployment(self, options: Dict) -> int:
        """Run enhanced deployment with all features"""
        print(f"{Fore.CYAN}🚀 Enhanced Deployment Mode{Style.RESET_ALL}")

        # Load configuration
        config_manager = EnhancedConfigManager(self.config_path)
        config = config_manager.load_config()

        # Apply template if specified
        if options.get('template'):
            config = self._apply_template_config(config, options['template'])

        # Validate configuration
        is_valid, errors = config_manager.validate_config()
        if not is_valid:
            print(f"{Fore.RED}❌ Configuration validation failed:{Style.RESET_ALL}")
            for error in errors:
                print(f"   • {error}")
            return 1

        # Initialize deployer
        deployer = EnhancedConxianDeployer(config, options.get('verbose', False))

        # Run pre-deployment checks
        if not options.get('skip_checks'):
            print("🔍 Running comprehensive pre-deployment checks...")
            if not deployer.run_pre_checks():
                if not options.get('force'):
                    print(f"{Fore.RED}❌ Pre-deployment checks failed.{Style.RESET_ALL}")
                    print("💡 Use --force to continue anyway")
                    return 1

        # Execute deployment
        print(f"🚀 Starting deployment...")
        results = deployer.deploy_conxian(
            category=options.get('category'),
            dry_run=options.get('dry_run', False)
        )

        # Show results
        if options.get('dry_run'):
            print(f"\n{Fore.GREEN}✅ Dry run completed successfully{Style.RESET_ALL}")
        else:
            print(f"\n📊 Deployment Results:")
            print(f"   ✅ Successful: {len(results.get('successful', []))}")
            print(f"   ❌ Failed: {len(results.get('failed', []))}")
            print(f"   ⏭️  Skipped: {len(results.get('skipped', []))}")

            if results.get('failed'):
                print(f"\n{Fore.RED}❌ Failed contracts:{Style.RESET_ALL}")
                for failed in results['failed']:
                    print(f"   • {failed['name']}: {failed['error']}")
                return 1

            print(f"\n{Fore.GREEN}🎉 Deployment completed successfully!{Style.RESET_ALL}")
            print("💡 Run 'stacksorbit monitor --follow' to track confirmations")

        return 0

    def run_enhanced_monitoring(self, options: Dict) -> int:
        """Run enhanced monitoring"""
        print(f"{Fore.CYAN}📊 Enhanced Monitoring Mode{Style.RESET_ALL}")

        # Load configuration
        config_manager = EnhancedConfigManager(self.config_path)
        config = config_manager.load_config()

        if options.get('dashboard'):
            # Run dashboard
            dashboard = EnhancedDashboard(config, config.get('NETWORK', 'testnet'))
            dashboard.start_dashboard()
            return 0

        else:
            # Run command-line monitoring
            monitor = DeploymentMonitor(config.get('NETWORK', 'testnet'), config)

            # Show API status
            api_status = monitor.check_api_status()
            print(f"🌐 API Status: {api_status['status']}")
            print(f"   Network: {api_status.get('network_id', 'unknown')}")
            print(f"   Block Height: {api_status.get('block_height', 0)}")

            address = config.get('SYSTEM_ADDRESS')
            if address:
                print(f"\n👤 Account Status:")
                account_info = monitor.get_account_info(address)
                if account_info:
                    balance = int(account_info.get('balance', 0)) / 1000000
                    print(f"   Balance: {balance} STX")
                    print(f"   Nonce: {account_info.get('nonce', 0)}")

                print(f"\n📦 Deployed Contracts:")
                contracts = monitor.get_deployed_contracts(address)
                print(f"   Count: {len(contracts)}")

                if contracts:
                    print("   Recent contracts:")
                    for contract in contracts[-5:]:  # Show last 5
                        print(f"     - {contract.get('contract_id', 'unknown')}")

            if options.get('follow'):
                print(f"\n🔄 Starting real-time monitoring...")
                print("📝 Press Ctrl+C to stop")

                monitor_thread = monitor.start_monitoring()

                try:
                    while monitor.is_monitoring:
                        time.sleep(1)
                except KeyboardInterrupt:
                    pass

                monitor.stop_monitoring()
                print("✅ Monitoring stopped")

            return 0

    def run_enhanced_verification(self, options: Dict) -> int:
        """Run enhanced verification"""
        print(f"{Fore.CYAN}🔍 Enhanced Verification Mode{Style.RESET_ALL}")

        # Load configuration
        config_manager = EnhancedConfigManager(self.config_path)
        config = config_manager.load_config()

        address = config.get('SYSTEM_ADDRESS')
        if not address:
            print(f"{Fore.RED}❌ SYSTEM_ADDRESS not configured{Style.RESET_ALL}")
            return 1

        # Get expected contracts
        expected_contracts = options.get('contracts')
        if not expected_contracts:
            # Try to load from Clarinet.toml
            from deployment_verifier import load_expected_contracts
            expected_contracts = load_expected_contracts()

        if not expected_contracts:
            print(f"{Fore.YELLOW}⚠️  No contracts specified for verification{Style.RESET_ALL}")
            return 1

        # Initialize verifier
        verifier = DeploymentVerifier(
            network=config.get('NETWORK', 'testnet'),
            config=config
        )

        # Run comprehensive verification
        results = verifier.run_comprehensive_verification(expected_contracts)

        # Print detailed summary
        verifier.print_verification_summary()

        # Exit with appropriate code
        return 0 if results['overall_status'] == 'success' else 1

    def run_enhanced_dashboard(self, options: Dict) -> int:
        """Run enhanced dashboard"""
        print(f"{Fore.CYAN}📊 Enhanced Dashboard Mode{Style.RESET_ALL}")

        # Load configuration
        config_manager = EnhancedConfigManager(self.config_path)
        config = config_manager.load_config()

        # Start dashboard
        dashboard = EnhancedDashboard(config, config.get('NETWORK', 'testnet'))
        dashboard.start_dashboard()

        return 0

    def run_comprehensive_diagnosis(self, options: Dict) -> int:
        """Run comprehensive system diagnosis"""
        print(f"{Fore.CYAN}🔍 Comprehensive System Diagnosis{Style.RESET_ALL}")
        print("=" * 60)

        # Load configuration
        config_manager = EnhancedConfigManager(self.config_path)
        config = config_manager.load_config()

        diagnosis = {
            'timestamp': datetime.now().isoformat(),
            'system_status': 'unknown',
            'issues': [],
            'recommendations': [],
            'scores': {}
        }

        # 1. Configuration Check
        print("🔧 Configuration Check...")
        try:
            is_valid, errors = config_manager.validate_config()
            if is_valid:
                print(f"{Fore.GREEN}✅ Configuration valid{Style.RESET_ALL}")
                diagnosis['scores']['config'] = 100
            else:
                print(f"{Fore.RED}❌ Configuration issues: {errors}{Style.RESET_ALL}")
                diagnosis['issues'].extend(errors)
                diagnosis['scores']['config'] = 0
        except Exception as e:
            print(f"{Fore.RED}❌ Configuration error: {e}{Style.RESET_ALL}")
            diagnosis['issues'].append(str(e))
            diagnosis['scores']['config'] = 0

        # 2. Network Check
        print("🌐 Network Check...")
        try:
            monitor = DeploymentMonitor(config.get('NETWORK', 'testnet'), config)
            api_status = monitor.check_api_status()
            if api_status['status'] == 'online':
                print(f"{Fore.GREEN}✅ Network connectivity: {api_status['network_id']}{Style.RESET_ALL}")
                diagnosis['scores']['network'] = 100
            else:
                print(f"{Fore.RED}❌ Network issue: {api_status.get('error', 'Unknown')}{Style.RESET_ALL}")
                diagnosis['issues'].append(f"Network connectivity: {api_status.get('error', 'Unknown')}")
                diagnosis['scores']['network'] = 0
        except Exception as e:
            print(f"{Fore.RED}❌ Network error: {e}{Style.RESET_ALL}")
            diagnosis['issues'].append(str(e))
            diagnosis['scores']['network'] = 0

        # 3. Account Check
        address = config.get('SYSTEM_ADDRESS')
        if address:
            print("👤 Account Check...")
            try:
                account_info = monitor.get_account_info(address)
                if account_info:
                    balance = int(account_info.get('balance', 0)) / 1000000
                    print(f"{Fore.GREEN}✅ Account balance: {balance} STX{Style.RESET_ALL}")
                    diagnosis['scores']['account'] = min(100, balance * 10)  # Score based on balance
                else:
                    print(f"{Fore.YELLOW}⚠️  Could not check account balance{Style.RESET_ALL}")
                    diagnosis['scores']['account'] = 50
            except Exception as e:
                print(f"{Fore.RED}❌ Account check error: {e}{Style.RESET_ALL}")
                diagnosis['issues'].append(str(e))
                diagnosis['scores']['account'] = 0
        else:
            print(f"{Fore.YELLOW}⚠️  No address configured{Style.RESET_ALL}")
            diagnosis['issues'].append("SYSTEM_ADDRESS not configured")
            diagnosis['scores']['account'] = 0

        # 4. Contract Analysis
        print("📦 Contract Analysis...")
        try:
            deployer = EnhancedConxianDeployer(config, options.get('verbose', False))
            contracts = deployer._get_deployment_list()
            if contracts:
                print(f"{Fore.GREEN}✅ Found {len(contracts)} contracts{Style.RESET_ALL}")
                diagnosis['scores']['contracts'] = 100
            else:
                print(f"{Fore.YELLOW}⚠️  No contracts found{Style.RESET_ALL}")
                diagnosis['issues'].append("No contracts found")
                diagnosis['scores']['contracts'] = 0
        except Exception as e:
            print(f"{Fore.RED}❌ Contract analysis error: {e}{Style.RESET_ALL}")
            diagnosis['issues'].append(str(e))
            diagnosis['scores']['contracts'] = 0

        # 5. Dependencies Check
        print("🔗 Dependencies Check...")
        try:
            import subprocess
            deps_ok = True

            # Check Python dependencies
            python_deps = ['requests', 'toml', 'pyyaml']
            for dep in python_deps:
                try:
                    __import__(dep)
                except ImportError:
                    print(f"{Fore.RED}❌ Missing Python dependency: {dep}{Style.RESET_ALL}")
                    deps_ok = False

            # Check Node.js dependencies
            try:
                result = subprocess.run(['node', '--version'], capture_output=True, timeout=5)
                if result.returncode == 0:
                    print(f"{Fore.GREEN}✅ Node.js available{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}❌ Node.js not available{Style.RESET_ALL}")
                    deps_ok = False
            except:
                print(f"{Fore.RED}❌ Node.js not available{Style.RESET_ALL}")
                deps_ok = False

            if deps_ok:
                print(f"{Fore.GREEN}✅ All dependencies available{Style.RESET_ALL}")
                diagnosis['scores']['dependencies'] = 100
            else:
                diagnosis['issues'].append("Missing dependencies")
                diagnosis['scores']['dependencies'] = 0

        except Exception as e:
            print(f"{Fore.RED}❌ Dependencies check error: {e}{Style.RESET_ALL}")
            diagnosis['issues'].append(str(e))
            diagnosis['scores']['dependencies'] = 0

        # Calculate overall score
        total_score = sum(diagnosis['scores'].values())
        max_score = len(diagnosis['scores']) * 100
        overall_percentage = (total_score / max_score) * 100 if max_score > 0 else 0

        diagnosis['overall_score'] = overall_percentage

        if overall_percentage >= 90:
            diagnosis['system_status'] = 'excellent'
        elif overall_percentage >= 70:
            diagnosis['system_status'] = 'good'
        elif overall_percentage >= 50:
            diagnosis['system_status'] = 'fair'
        else:
            diagnosis['system_status'] = 'poor'

        # Generate recommendations
        if diagnosis['scores'].get('config', 0) < 100:
            diagnosis['recommendations'].append("Fix configuration issues")

        if diagnosis['scores'].get('network', 0) < 100:
            diagnosis['recommendations'].append("Check network connectivity")

        if diagnosis['scores'].get('account', 0) < 50:
            diagnosis['recommendations'].append("Fund your Stacks account")

        if diagnosis['scores'].get('contracts', 0) < 100:
            diagnosis['recommendations'].append("Add or fix contract files")

        # Print diagnosis summary
        print(f"\n📊 Diagnosis Summary:")
        print(f"   Overall Status: {diagnosis['system_status'].upper()}")
        print(f"   Overall Score: {overall_percentage:.1f}%")

        print(f"\n📋 Component Scores:")
        for component, score in diagnosis['scores'].items():
            status_icon = "✅" if score >= 80 else "⚠️" if score >= 50 else "❌"
            print(f"   {status_icon} {component.capitalize()}: {score}%")

        if diagnosis['issues']:
            print(f"\n❌ Issues Found:")
            for issue in diagnosis['issues']:
                print(f"   • {issue}")

        if diagnosis['recommendations']:
            print(f"\n💡 Recommendations:")
            for rec in diagnosis['recommendations']:
                print(f"   • {rec}")

        # Save diagnosis
        diagnosis_path = Path("logs") / f"diagnosis_{int(time.time())}.json"
        diagnosis_path.parent.mkdir(exist_ok=True)
        with open(diagnosis_path, 'w') as f:
            json.dump(diagnosis, f, indent=2)

        print(f"\n💾 Diagnosis saved to {diagnosis_path}")

        # Overall assessment
        if overall_percentage >= 90:
            print(f"\n{Fore.GREEN}🎉 System is ready for deployment!{Style.RESET_ALL}")
            print("💡 Run: stacksorbit deploy --dry-run")
        elif overall_percentage >= 70:
            print(f"\n{Fore.YELLOW}⚠️  System mostly ready, but has some issues.{Style.RESET_ALL}")
            print("💡 Fix the issues above, then try deployment")
        else:
            print(f"\n{Fore.RED}❌ System needs significant fixes before deployment.{Style.RESET_ALL}")
            print("💡 Address the issues above first")

        return 0

    def apply_deployment_template(self, options: Dict) -> int:
        """Apply deployment template"""
        template_name = options.get('name')
        if not template_name:
            print(f"{Fore.RED}❌ Template name required{Style.RESET_ALL}")
            print("Available templates:")
            for name, template in self.templates.get('templates', {}).items():
                print(f"  • {name} - {template['name']}")
            return 1

        templates = self.templates.get('templates', {})
        if template_name not in templates:
            print(f"{Fore.RED}❌ Template '{template_name}' not found{Style.RESET_ALL}")
            return 1

        template = templates[template_name]

        print(f"📋 Applying template: {Fore.CYAN}{template['name']}{Style.RESET_ALL}")
        print(f"📝 Description: {template['description']}")

        if template.get('warning'):
            print(f"{Fore.RED}⚠️  WARNING: {template['warning']}{Style.RESET_ALL}")

        print(f"\n⚙️  Configuration:")
        config = template['config']
        for key, value in config.items():
            print(f"   {key}: {value}")

        print(f"\n📋 Deployment Steps:")
        for i, step in enumerate(template['steps'], 1):
            print(f"   {i}. {step}")

        # Apply template to configuration
        config_manager = EnhancedConfigManager(self.config_path)
        current_config = config_manager.load_config()

        # Update with template config
        current_config.update(config)

        # Save updated configuration
        config_manager.save_config(current_config)

        print(f"\n✅ Template applied!")
        print(f"💾 Updated configuration saved to {self.config_path}")

        return 0

    def run_devnet(self, options: Dict) -> int:
        """Run local development network"""
        config_manager = EnhancedConfigManager(self.config_path)
        config = config_manager.load_config()
        stacks_core_path = Path(config.get("STACKS_CORE_PATH", self.project_root / "stacks-core"))
        devnet = LocalDevnet(stacks_core_path)
        command = options.get("devnet_command")

        if command == "start":
            devnet.start()
        elif command == "stop":
            devnet.stop()
        elif command == "status":
            if devnet.is_running():
                print("Local development network is running.")
            else:
                print("Local development network is not running.")
        else:
            print("Invalid devnet command. Please use start, stop, or status.")
            return 1

        return 0

    def _apply_template_config(self, config: Dict, template_name: str) -> Dict:
        """Apply template configuration to existing config"""
        templates = self.templates.get('templates', {})
        if template_name in templates:
            template_config = templates[template_name]['config']
            config.update(template_config)

        return config

    def show_help(self):
        """Show comprehensive help"""
        print(f"{Fore.CYAN}🚀 Ultimate StacksOrbit - Enhanced Deployment Tool{Style.RESET_ALL}")
        print("=" * 70)
        print()
        print("Usage:")
        print("  stacksorbit <command> [options]")
        print()
        print("Commands:")
        print("  setup           Run interactive setup wizard")
        print("  deploy          Deploy contracts with enhanced features")
        print("  monitor         Monitor deployment with real-time dashboard")
        print("  verify          Verify deployment completeness")
        print("  dashboard       Launch enhanced monitoring dashboard")
        print("  diagnose        Run comprehensive system diagnosis")
        print("  template        Apply deployment template")
        print()
        print("Deployment Options:")
        print("  --category <cat>    Deploy specific category (base, core, tokens, etc.)")
        print("  --template <name>   Use deployment template")
        print("  --batch-size <n>    Contracts per batch (default: 5)")
        print("  --dry-run           Test deployment without executing")
        print("  --skip-checks       Skip pre-deployment checks")
        print("  --force             Force deployment despite check failures")
        print("  --verbose           Enable detailed logging")
        print()
        print("Monitoring Options:")
        print("  --follow            Follow deployment in real-time")
        print("  --dashboard         Launch interactive dashboard")
        print("  --api-only          Check only API status")
        print()
        print("Verification Options:")
        print("  --contracts <list>  Specific contracts to verify")
        print("  --comprehensive     Run comprehensive verification")
        print()
        print("Examples:")
        print("  # Quick setup")
        print("  stacksorbit setup")
        print()
        print("  # Deploy with template")
        print("  stacksorbit deploy --template testnet_quick_start")
        print()
        print("  # Deploy specific category")
        print("  stacksorbit deploy --category core --dry-run")
        print()
        print("  # Monitor in real-time")
        print("  stacksorbit monitor --follow --dashboard")
        print()
        print("  # Comprehensive verification")
        print("  stacksorbit verify --comprehensive")
        print()
        print("  # Full diagnosis")
        print("  stacksorbit diagnose --verbose")
        print()
        print("Available Templates:")
        templates = self.templates.get('templates', {})
        if templates:
            for name, template in templates.items():
                print(f"  • {name} - {template['name']}")
        else:
            print("  No templates available")
        print()
        print(f"{Fore.GREEN}🚀 Ready to deploy to Stacks blockchain!{Style.RESET_ALL}")

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description='Ultimate StacksOrbit - Enhanced Deployment Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('command', nargs='?', help='Command to execute')
    parser.add_argument('--config', default='.env', help='Configuration file path')
    parser.add_argument('--network', choices=['devnet', 'testnet', 'mainnet'], default='testnet')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    # Deployment options
    parser.add_argument('--category', choices=['base', 'core', 'tokens', 'dex', 'dimensional', 'oracle', 'governance', 'security', 'monitoring'])
    parser.add_argument('--template', help='Deployment template name')
    parser.add_argument('--batch-size', type=int, default=5, help='Contracts per batch')
    parser.add_argument('--dry-run', action='store_true', help='Dry run deployment')
    parser.add_argument('--skip-checks', action='store_true', help='Skip pre-deployment checks')
    parser.add_argument('--force', action='store_true', help='Force deployment')

    # Monitoring options
    parser.add_argument('--follow', action='store_true', help='Follow in real-time')
    parser.add_argument('--dashboard', action='store_true', help='Launch dashboard')
    parser.add_argument('--api-only', action='store_true', help='API status only')

    # Verification options
    parser.add_argument('--contracts', nargs='*', help='Contracts to verify')
    parser.add_argument('--comprehensive', action='store_true', help='Comprehensive verification')

    # Devnet options
    parser.add_argument('--devnet-command', choices=['start', 'stop', 'status'], help='Local development network command')

    args = parser.parse_args()

    try:
        # Initialize ultimate deployer
        deployer = UltimateStacksOrbit()

        # Convert args to dict
        options = {
            'category': args.category,
            'template': args.template,
            'batch_size': args.batch_size,
            'dry_run': args.dry_run,
            'skip_checks': args.skip_checks,
            'force': args.force,
            'follow': args.follow,
            'dashboard': args.dashboard,
            'api_only': args.api_only,
            'contracts': args.contracts,
            'comprehensive': args.comprehensive,
            'verbose': args.verbose,
            'devnet_command': args.devnet_command
        }

        # Execute command
        if args.command:
            return deployer.run_command(args.command, **options)
        else:
            deployer.show_help()
            return 0

    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}🛑 Operation cancelled by user{Style.RESET_ALL}")
        return 1
    except Exception as e:
        print(f"\n{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())
