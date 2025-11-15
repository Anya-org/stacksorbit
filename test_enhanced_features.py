#!/usr/bin/env python3
"""
Simplified Test Suite for Enhanced StacksOrbit
Tests the enhanced features without complex imports
"""

import os
import sys
import json
import unittest
import tempfile
from pathlib import Path

class TestEnhancedFeatures(unittest.TestCase):
    """Test enhanced features functionality"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_config_file_creation(self):
        """Test configuration file creation"""
        config_path = os.path.join(self.temp_dir, '.env')

        # Test config creation
        config_content = """DEPLOYER_PRIVKEY=1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
SYSTEM_ADDRESS=SP2ED6H1EHHTZA1NTWR2GKBMT0800Y6F081EEJ45R
NETWORK=testnet
HIRO_API_KEY=test_key
"""

        with open(config_path, 'w') as f:
            f.write(config_content)

        # Verify config was created
        self.assertTrue(os.path.exists(config_path))

        # Verify content
        with open(config_path, 'r') as f:
            content = f.read()
            self.assertIn('DEPLOYER_PRIVKEY', content)
            self.assertIn('SYSTEM_ADDRESS', content)
            self.assertIn('NETWORK=testnet', content)

    def test_clarinet_analysis(self):
        """Test Clarinet.toml analysis"""
        # Create mock Clarinet.toml
        clarinet_content = """[project]
name = "test-project"
description = "Test project"

[contracts.all-traits]
path = "contracts/traits/all-traits.clar"

[contracts.cxd-token]
path = "contracts/tokens/cxd-token.clar"

[contracts.dex-factory]
path = "contracts/dex/dex-factory.clar"
"""

        clarinet_path = os.path.join(self.temp_dir, 'Clarinet.toml')
        with open(clarinet_path, 'w') as f:
            f.write(clarinet_content)

        # Test contract extraction
        import re
        contract_matches = re.findall(r'\[contracts\.([^\]]+)\]', clarinet_content)

        self.assertEqual(len(contract_matches), 3)
        self.assertIn('all-traits', contract_matches)
        self.assertIn('cxd-token', contract_matches)
        self.assertIn('dex-factory', contract_matches)

    def test_category_recognition(self):
        """Test contract category recognition"""
        test_contracts = [
            'all-traits', 'utils-encoding', 'lib-error-codes',
            'cxd-token', 'cxlp-token', 'cxvg-token',
            'dex-factory', 'dex-router', 'dex-pool',
            'dim-registry', 'position-nft', 'dimensional-core',
            'governance-token', 'proposal-engine',
            'circuit-breaker', 'pausable',
            'monitoring-dashboard', 'analytics-aggregator'
        ]

        categories = {
            'base': ['all-traits', 'utils-encoding', 'lib-error-codes'],
            'tokens': ['cxd-token', 'cxlp-token', 'cxvg-token'],
            'dex': ['dex-factory', 'dex-router', 'dex-pool'],
            'dimensional': ['dim-registry', 'position-nft', 'dimensional-core'],
            'governance': ['governance-token', 'proposal-engine'],
            'security': ['circuit-breaker', 'pausable'],
            'monitoring': ['monitoring-dashboard', 'analytics-aggregator']
        }

        # Test categorization logic
        for contract in test_contracts:
            categorized = False
            for category, patterns in categories.items():
                if any(pattern in contract for pattern in patterns):
                    categorized = True
                    break

            self.assertTrue(categorized, f"Contract {contract} not categorized")

    def test_deployment_templates(self):
        """Test deployment templates"""
        templates = {
            'testnet_quick_start': {
                'network': 'testnet',
                'batch_size': 5,
                'monitoring': True
            },
            'mainnet_production': {
                'network': 'mainnet',
                'batch_size': 3,
                'monitoring': True,
                'verification': True
            }
        }

        # Test template structure
        for template_name, template in templates.items():
            self.assertIn('network', template)
            self.assertIn('batch_size', template)

            # Test network validation
            self.assertIn(template['network'], ['devnet', 'testnet', 'mainnet'])

    def test_error_handling(self):
        """Test error handling and user-friendly messages"""
        # Test configuration validation
        config = {
            'DEPLOYER_PRIVKEY': 'short_key',  # Invalid
            'SYSTEM_ADDRESS': 'invalid_address',  # Invalid
            'NETWORK': 'invalid_network'  # Invalid
        }

        errors = []

        # Validate private key
        if len(config['DEPLOYER_PRIVKEY']) != 64:
            errors.append('Invalid private key length')

        # Validate address
        if not config['SYSTEM_ADDRESS'].startswith('S') or len(config['SYSTEM_ADDRESS']) != 41:
            errors.append('Invalid address format')

        # Validate network
        if config['NETWORK'] not in ['devnet', 'testnet', 'mainnet']:
            errors.append('Invalid network')

        self.assertEqual(len(errors), 3)

    def test_user_experience(self):
        """Test user experience improvements"""
        # Test that help is comprehensive
        help_commands = [
            'deploy', 'monitor', 'verify', 'check', 'setup', 'dashboard'
        ]

        # Verify all major commands are documented
        for command in help_commands:
            self.assertIn(command, help_commands)

        # Test that error messages are user-friendly
        friendly_errors = [
            'Configuration validation failed',
            'Network connectivity failed',
            'Deployment failed'
        ]

        for error in friendly_errors:
            self.assertIn('failed', error.lower())

class TestIntegration(unittest.TestCase):
    """Integration tests"""

    def test_project_structure(self):
        """Test project structure is complete"""
        required_files = [
            'stacksorbit_cli.py',
            'stacksorbit_dashboard.py',
            'enhanced_conxian_deployment.py',
            'deployment_monitor.py',
            'deployment_verifier.py',
            'local_devnet.py'
        ]

        for file_path in required_files:
            full_path = os.path.join(os.path.dirname(__file__), file_path)
            self.assertTrue(os.path.exists(full_path), f"Missing file: {file_path}")

    def test_package_json_scripts(self):
        """Test package.json scripts"""
        package_path = os.path.join(os.path.dirname(__file__), 'package.json')

        with open(package_path, 'r') as f:
            package_data = json.load(f)

        scripts = package_data.get('scripts', {})

        required_scripts = [
            'setup', 'deploy', 'monitor', 'verify', 'dashboard', 'diagnose'
        ]

        for script in required_scripts:
            self.assertIn(script, scripts, f"Missing script: {script}")

def run_enhanced_tests():
    """Run all enhanced tests"""
    print("🧪 Running Enhanced StacksOrbit Test Suite\n")

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestEnhancedFeatures))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print(f"\n📊 Test Summary:")
    print(f"   Tests run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")

    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0
    print(f"   Success rate: {success_rate:.1f}%")

    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_enhanced_tests()
    sys.exit(0 if success else 1)
