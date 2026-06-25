import time
import functools
from conxius_orbit_secrets import is_sensitive_key, _is_sensitive_normalized
from deployment_monitor import DeploymentMonitor


def benchmark_secrets():
    print("--- Benchmarking Secrets Cache ---")
    # Using more iterations to get measurable numbers
    keys = ["key", "KEY", "Key", "key_token", "KEY_TOKEN", "Key_Token"] * 10000

    start = time.perf_counter()
    for k in keys:
        is_sensitive_key(k)
    end = time.perf_counter()
    print(f"Mixed case run (redundant caching): {end - start:.4f}s")

    # After normalization optimization, this should be faster as it skips the outer cache layer
    # and hits the normalized cache directly.


def benchmark_monitor():
    print("\n--- Benchmarking Monitor Cache ---")
    monitor = DeploymentMonitor(network="testnet")
    # Clear cache to ensure we see the behavior
    monitor.cache = {}
    monitor.redacted_cache = {}

    tx_id = "1" * 64
    tx_id_0x = "0x" + tx_id

    # Mocking session.get to avoid network calls during benchmark
    calls = 0

    def mock_get(*args, **kwargs):
        nonlocal calls
        calls += 1

        class MockResponse:
            def json(self):
                return {"tx_status": "success"}

            def raise_for_status(self):
                pass

            @property
            def status_code(self):
                return 200

        return MockResponse()

    monitor.session.get = mock_get

    monitor.get_transaction_info(tx_id)
    monitor.get_transaction_info(tx_id_0x)

    print(
        f"Number of API calls for same TX ID (with/without 0x): {calls} (Expected: 2 before optimization)"
    )

    # Currently, they generate different keys, so both miss and hit the 'API'


if __name__ == "__main__":
    benchmark_secrets()
    benchmark_monitor()
