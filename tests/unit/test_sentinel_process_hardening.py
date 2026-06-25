import os
import json
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from scripts.enhanced_conxian_deployment import EnhancedConxianDeployer
from conxius_orbit_secrets import is_sensitive_key, redact_recursive


def test_api_key_redaction_expansion():
    """🛡️ Sentinel: Verify that APIKEY and API_KEY are now redacted even with public prefixes."""
    assert is_sensitive_key("PUBLIC_API_KEY") is True
    assert is_sensitive_key("ADDR_APIKEY") is True

    config = {"PUBLIC_API_KEY": "secret-api-123", "ADDR_APIKEY": "secret-api-456"}
    redacted = redact_recursive(config)
    assert redacted["PUBLIC_API_KEY"] == "<redacted>"
    assert redacted["ADDR_APIKEY"] == "<redacted>"


def test_deploy_single_contract_env_hardening():
    """🛡️ Sentinel: Verify that DEPLOYER_PRIVKEY is passed via env and removed from CLI args."""
    config = {
        "DEPLOYER_PRIVKEY": "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        "NETWORK": "testnet",
        "SYSTEM_ADDRESS": "ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM",
    }
    deployer = EnhancedConxianDeployer(config)

    contract = {"name": "my-contract", "path": "contracts/my-contract.clar"}

    # Mock Path and subprocess.run
    with patch("scripts.enhanced_conxian_deployment.Path") as mock_path:
        # Set up mock_path to make the script and contract files "exist"
        mock_js_script = MagicMock()
        mock_js_script.exists.return_value = True

        mock_contract_path = MagicMock()
        mock_contract_path.exists.return_value = True

        # This is a bit tricky because Path is called multiple times.
        # We've got js_script and contract_path.
        def side_effect(arg):
            if "execute_deploy.js" in str(arg):
                return mock_js_script
            if "Conxian" in str(arg) or "contracts" in str(arg):
                return mock_contract_path
            return MagicMock()

        mock_path.side_effect = side_effect

        with patch("scripts.enhanced_conxian_deployment.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout=json.dumps({"success": True, "txId": "0x123"}), returncode=0
            )

            tx_id = deployer._deploy_single_contract(contract)

            assert tx_id == "0x123"

            # Verify subprocess.run call
            args, kwargs = mock_run.call_args
            cmd = args[0]

            # Check that DEPLOYER_PRIVKEY is NOT in the command list
            assert config["DEPLOYER_PRIVKEY"] not in cmd

            # Check that DEPLOYER_PRIVKEY IS in the env parameter
            assert "env" in kwargs
            assert kwargs["env"]["DEPLOYER_PRIVKEY"] == config["DEPLOYER_PRIVKEY"]
            # Ensure other env vars are preserved
            assert "PATH" in kwargs["env"]
