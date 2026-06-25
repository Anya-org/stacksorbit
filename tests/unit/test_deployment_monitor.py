import unittest
from unittest.mock import patch, MagicMock
import time
import os
import sys
import tempfile
from pathlib import Path

# Add parent directory to path to import modules
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from deployment_monitor import DeploymentMonitor


class TestDeploymentMonitorCache(unittest.TestCase):
    """Tests for the caching functionality in DeploymentMonitor."""

    def setUp(self):
        """Set up a DeploymentMonitor instance for testing."""
        # Use a temporary cache file for testing to avoid interference
        self.test_cache_path = "logs/test_api_cache.json"
        if os.path.exists(self.test_cache_path):
            os.remove(self.test_cache_path)

        self.monitor = DeploymentMonitor(
            network="testnet", config={"LOG_LEVEL": "DEBUG"}
        )
        self.monitor.cache_path = Path(self.test_cache_path)
        self.monitor.cache = {}  # Start with empty cache
        # Lower the expiry for faster testing
        self.monitor.cache_expiry = 2

    def tearDown(self):
        """Clean up after testing."""
        if os.path.exists(self.test_cache_path):
            os.remove(self.test_cache_path)

    @patch("requests.Session.get")
    def test_get_recent_transactions_caching(self, mock_get):
        """Verify that get_recent_transactions caches results."""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": [{"tx_id": "0x123"}]}
        mock_get.return_value = mock_response

        address = "ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM"

        # --- First call (should hit API) ---
        result1 = self.monitor.get_recent_transactions(address)
        self.assertEqual(len(result1), 1)
        self.assertEqual(result1[0]["tx_id"], "0x123")
        mock_get.assert_called_once()

        # --- Second call (should be cached) ---
        result2 = self.monitor.get_recent_transactions(address)
        self.assertEqual(len(result2), 1)
        # The mock should still have been called only once
        mock_get.assert_called_once()

        # --- Wait for cache to expire ---
        time.sleep(self.monitor.cache_expiry + 0.1)

        # --- Third call (should hit API again) ---
        result3 = self.monitor.get_recent_transactions(address)
        self.assertEqual(len(result3), 1)
        # The mock should now have been called a second time
        self.assertEqual(mock_get.call_count, 2)

    def test_load_cache_malformed_json_without_logger(self):
        """Malformed cache JSON should safely fall back even without self.logger."""
        with open(self.test_cache_path, "w", encoding="utf-8") as cache_file:
            cache_file.write("{not-valid-json")

        if hasattr(self.monitor, "logger"):
            delattr(self.monitor, "logger")

        loaded_cache = self.monitor._load_cache()
        self.assertEqual(loaded_cache, {})


class TestDeploymentMonitorInitialization(unittest.TestCase):
    """Initialization behavior with malformed cache files."""

    def test_init_handles_malformed_default_cache_file(self):
        """DeploymentMonitor init should not crash when logs/api_cache.json is malformed."""
        original_cwd = os.getcwd()

        with tempfile.TemporaryDirectory() as temp_dir:
            os.chdir(temp_dir)
            try:
                os.makedirs("logs", exist_ok=True)
                with open("logs/api_cache.json", "w", encoding="utf-8") as cache_file:
                    cache_file.write("{invalid-json")

                monitor = DeploymentMonitor(
                    network="testnet",
                    config={"LOG_LEVEL": "DEBUG", "SAVE_LOGS": "false"},
                )

                self.assertEqual(monitor.cache, {})
            finally:
                os.chdir(original_cwd)


if __name__ == "__main__":
    unittest.main()
