import timeit
import functools
import re


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


_CONTRACT_CAT_PATTERNS = [
    (re.compile(r"dex|swap|pool|factory|router|amm|liquidity"), "dex"),
    (re.compile(r"trait|utils|lib|error|constant|math|std"), "base"),
    (re.compile(r"token|ft-|sip-010"), "tokens"),
    (re.compile(r"nft|non-fungible|sip-009"), "nft"),
    (re.compile(r"oracle|aggregator|price|feed"), "oracle"),
    (re.compile(r"gov|vote|proposal|dao|multisig|treasury"), "governance"),
    (re.compile(r"security|auth|access|guardian|pause|whitelist"), "security"),
    (re.compile(r"monitor|track|dashboard|analytics|registry"), "monitoring"),
]


@functools.lru_cache(maxsize=2048)
def _categorize_contract_regex_cached(name_casefold: str) -> str:
    for regex, category in _CONTRACT_CAT_PATTERNS:
        if regex.search(name_casefold):
            return category
    return "other"


if __name__ == "__main__":
    names = [
        "my-awesome-dex-token-contract",
        "my-awesome-DEX-token-contract",
        "sip-010-ft-token",
        "dao-gov-proposal",
        "oracle-price-feed",
        "nft-sip-009-non-fungible",
        "monitoring-dashboard-analytics",
        "base-utils-trait-lib",
    ]

    def run_original() -> None:
        for name in names:
            _categorize_contract_original(name)

    def run_cache_only() -> None:
        for name in names:
            _categorize_contract_cached(name)

    def run_regex_cache() -> None:
        for name in names:
            _categorize_contract_regex_cached(name.casefold())

    rounds = 25000

    _categorize_contract_cached.cache_clear()
    _categorize_contract_regex_cached.cache_clear()

    t1 = timeit.timeit(run_original, number=rounds)
    t2 = timeit.timeit(run_cache_only, number=rounds)
    t3 = timeit.timeit(run_regex_cache, number=rounds)

    print(f"Original:    {t1:.6f}s")
    print(f"Cache-only:  {t2:.6f}s")
    print(f"Regex+cache: {t3:.6f}s")
    print(f"Speedup vs original (regex+cache): {t1/t3:.2f}x")
