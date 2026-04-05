import time
import sys
import os
import threading
from typing import Dict, Optional
from infrastructure_wiring import InfrastructureWiring

# Mock requests.Session to avoid network calls
class MockResponse:
    def __init__(self, data, status_code=200):
        self._data = data
        self.status_code = status_code
    def json(self):
        return self._data

class MockSession:
    def __init__(self):
        self.get_count = 0
    def get(self, url, headers=None, timeout=None):
        self.get_count += 1
        time.sleep(0.1) # Simulate network latency
        if "runway_metrics" in url:
            return MockResponse([{"runway_months": 12}])
        elif "exit_velocity" in url:
            return MockResponse([{"current_estimated_valuation_zar": 1000000}])
        return MockResponse([])
    def post(self, url, headers=None, json=None, timeout=None):
        return MockResponse({}, 201)

def run_benchmark():
    print("⚡ Bolt: Initializing Infra Optimization Benchmark...")
    config = {
        "SUPABASE_URL": "https://mock.supabase.co",
        "SUPABASE_KEY": "mock-key"
    }

    infra = InfrastructureWiring(config)
    # Inject mock session
    infra.session = MockSession()

    print("\n--- Testing Cache and Connection Pooling ---")

    # 1. First call (Cache Miss)
    start = time.perf_counter()
    infra.get_runway_metrics()
    end = time.perf_counter()
    first_call_time = end - start
    print(f"First call (miss): {first_call_time:.4f}s")

    # 2. Second call (Cache Hit)
    start = time.perf_counter()
    infra.get_runway_metrics()
    end = time.perf_counter()
    second_call_time = end - start
    print(f"Second call (hit): {second_call_time:.4f}s")

    # Verification
    if second_call_time < first_call_time / 10:
        print("✅ Cache hit is significantly faster!")
    else:
        print("❌ Cache hit is NOT significantly faster!")

    if infra.session.get_count == 1:
        print("✅ Only 1 network call made for 2 requests!")
    else:
        print(f"❌ {infra.session.get_count} network calls made for 2 requests!")

    # 3. Test Exit Velocity Cache
    infra.get_exit_velocity()
    if infra.session.get_count == 2:
        infra.get_exit_velocity()
        if infra.session.get_count == 2:
            print("✅ Exit velocity cache working!")
        else:
             print("❌ Exit velocity cache NOT working!")

    print("\n--- Latency Reduction Analysis ---")
    print(f"Total time saved per UI refresh (cached): ~{0.2:.1f}s (2 x 100ms simulated latency)")
    print(f"Parallelization benefit in GUI: latency is max(T_blockchain, T_infra) instead of T_blockchain + T_infra_1 + T_infra_2")

if __name__ == "__main__":
    run_benchmark()
