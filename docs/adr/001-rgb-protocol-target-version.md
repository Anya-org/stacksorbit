# ADR 001: RGB Protocol Target Version

## Status
Proposed

## Context
Research into the RGB protocol (Session 50, CON-1338) has identified two incompatible forks:
1. **rgb-protocol org (v0.11.1 ecosystem):** Mainnet-ready, complete stack (consensus, wallet API, CLI, sandbox), supported by the RGB Protocol Association, and the target for Tether USDT.
2. **RGB-WG (v0.12):** Declared as rgb-core, but lacks wallets, CLI, and Lightning Network integration.

The current implementation of the RGB adapter (in related repositories or as planned) might have been targeting the v0.12 ecosystem due to its presence on crates.io.

## Decision
We will target the **rgb-protocol / rgb-lib v0.11.1 ecosystem** as the production target for ConxiusOrbit.

## Rationale
- **Maturity:** v0.11.1 has a full production stack and is used in live wallets (Iris, BitMask, etc.).
- **Ecosystem Support:** Supported by the official RGB Protocol Association and major industry players (Bitfinex, Tether).
- **Functionality:** native Lightning Network integration and support for all 5 core schemas (NIA, IFA, CFA, UDA, PFA).
- **Stability:** v0.12 is currently considered not production-ready by the broader ecosystem.

## Consequences
- We must ensure any crate dependencies or API calls align with `rgb-lib` v0.11.1.
- Implementation of contract state monitoring will use v0.11.1 patterns.
- Testing will utilize the `rgb-sandbox` (regtest).
- Implementation of RGB-WG v0.12 is explicitly out of scope for the immediate production roadmap.

## Revisit Conditions
This decision should be revisited if and when the v0.12 ecosystem achieves:
- A complete wallet and CLI stack.
- Stable Lightning Network integration.
- Broad industry adoption comparable to or exceeding v0.11.1.

## References
- Linear Issue: [CON-1338](https://linear.app/conxian-labs/issue/CON-1338/research-g-2g-21-rgb-protocol-fork-evaluation-and-production-adapter)
- Linear Issue: [CON-1356](https://linear.app/conxian-labs/issue/CON-1356/rgb-record-adr-selecting-rgb-lib-v0111-ecosystem-as-the-production)
