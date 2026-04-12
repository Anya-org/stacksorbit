import timeit
import functools

def _categorize_contract_original(name: str) -> str:
    name_lower = name.lower()
    if any(w in name_lower for w in ["dex", "swap", "pool", "factory", "router", "amm", "liquidity"]):
        return "dex"
    if any(w in name_lower for w in ["trait", "utils", "lib", "error", "constant", "math", "std"]):
        return "base"
    if any(w in name_lower for w in ["token", "ft-", "sip-010"]):
        return "tokens"
    if any(w in name_lower for w in ["nft", "non-fungible", "sip-009"]):
        return "nft"
    if any(w in name_lower for w in ["oracle", "aggregator", "price", "feed"]):
        return "oracle"
    if any(w in name_lower for w in ["gov", "vote", "proposal", "dao", "multisig", "treasury"]):
        return "governance"
    if any(w in name_lower for w in ["security", "auth", "access", "guardian", "pause", "whitelist"]):
        return "security"
    if any(w in name_lower for w in ["monitor", "track", "dashboard", "analytics", "registry"]):
        return "monitoring"
    return "other"

@functools.lru_cache(maxsize=128)
def _categorize_contract_cached(name: str) -> str:
    return _categorize_contract_original(name)

# Benchmark
name = "my-awesome-dex-token-contract"
n = 100000
t1 = timeit.timeit(lambda: _categorize_contract_original(name), number=n)
t2 = timeit.timeit(lambda: _categorize_contract_cached(name), number=n)

print(f"Original: {t1:.6f}s")
print(f"Cached:   {t2:.6f}s")
print(f"Speedup:  {t1/t2:.2f}x")
