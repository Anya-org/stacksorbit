import unittest
import os
import sys
import shutil
import tempfile
from pathlib import Path

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.enhanced_conxian_deployment import (
    EnhancedConxianDeployer,
    EnhancedConfigManager,
)
from scripts.deployment_verifier import DeploymentVerifier


class TestConxianFullIntegration(unittest.TestCase):
    """Full integration tests for Conxian using ConxiusOrbit"""

    @classmethod
    def setUpClass(cls):
        # Resolve integration workspace path portably:
        # 1) explicit override via CONXIAN_PATH
        # 2) otherwise use repository root inferred from this test file location
        conxian_path_env = os.environ.get("CONXIAN_PATH")
        if conxian_path_env:
            cls.conxian_path = Path(conxian_path_env).expanduser().resolve()
        else:
            cls.conxian_path = Path(__file__).resolve().parents[1]

        cls.conxius_orbit_path = cls.conxian_path

        clarinet_path = cls.conxian_path / "Clarinet.toml"
        if not clarinet_path.is_file():
            raise unittest.SkipTest(
                f"Conxian integration workspace unavailable: missing {clarinet_path}"
            )

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

        # Set mock secret in environment to bypass Sentinel .env check
        os.environ["DEPLOYER_PRIVKEY"] = (
            "mock_private_key_string_for_testing_purposes_only_1234567890abcde"
        )

        # Create a mock .env for testing (non-sensitive fields)
        self.config_path = Path(self.temp_dir) / ".env"
        with open(self.config_path, "w") as f:
            f.write("SYSTEM_ADDRESS=ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM\n")
            f.write("NETWORK=testnet\n")

        self.config_manager = EnhancedConfigManager(self.config_path)
        self.config = self.config_manager.load_config()

    def tearDown(self):
        if "DEPLOYER_PRIVKEY" in os.environ:
            del os.environ["DEPLOYER_PRIVKEY"]
        shutil.rmtree(self.temp_dir)

    def test_01_verify_clarinet_toml(self):
        """Test that Conxian Clarinet.toml is valid and parseable"""
        clarinet_path = self.conxian_path / "Clarinet.toml"
        self.assertTrue(clarinet_path.exists(), "Clarinet.toml should exist in Conxian")

        with open(clarinet_path, "r") as f:
            content = f.read()
            self.assertIn("[project]", content)
            self.assertIn('name = "ConxiusOrbit"', content)

    def test_02_deployment_simulation(self):
        """Test deployment simulation (dry-run)"""
        # We need to temporarily mock the current working directory or adjust the deployer
        # to accept a project path, but EnhancedConxianDeployer might depend on CWD.
        # Check if we can pass a path or if we need to chdir.

        # Saving CWD
        original_cwd = os.getcwd()
        try:
            os.chdir(self.conxian_path)

            deployer = EnhancedConxianDeployer(self.config, verbose=True)

            # Run pre-checks
            checks_passed = deployer.run_pre_checks()
            # In environments without Clarinet, we expect compilation check to fail but others to pass
            if not shutil.which("clarinet"):
                print(
                    "⚠️ Skipping strict checks_passed assertion as clarinet is missing"
                )
            else:
                self.assertTrue(checks_passed, "Pre-deployment checks should pass")

            # Run dry-run deployment
            results = deployer.deploy_conxian(category=None, dry_run=True)  # Deploy all

            self.assertTrue(results["success"], "Dry run should be successful")

        finally:
            os.chdir(original_cwd)

    def test_03_contract_verification(self):
        """Verify that expected contracts match Clarinet.toml"""

        # We'll use the DeploymentVerifier to check what it expects
        verifier = DeploymentVerifier(network="testnet", config=self.config)
        # Note: DeploymentVerifier.load_expected_contracts typically loads from a local file.
        # We might need to point it to Conxian's Clarinet.toml explicitly or ensure it uses it.

        # For this test, we verify that the verifier can at least init and validate structure
        # Assuming the verifier has logic to parse Clarinet.toml if we are in the dir

        original_cwd = os.getcwd()
        try:
            os.chdir(self.conxian_path)
            # Re-init verifier in the correct directory
            verifier = DeploymentVerifier(network="testnet", config=self.config)

            # It might fail if it can't find deployed contracts on chain (since we didn't deploy),
            # but we can check if it can load the expected contracts list correctly.

            # Using a private method or internal logic if available, otherwise just checking init
            # If load_expected_contracts is a standalone function in deployment_verifier.py:
            from scripts.deployment_verifier import load_expected_contracts

            expected = load_expected_contracts()
            self.assertTrue(len(expected) > 0, "Should find contracts in Clarinet.toml")
            self.assertIn("placeholder", expected, "Should find placeholder")

        finally:
            os.chdir(original_cwd)


if __name__ == "__main__":
    unittest.main()
