import os
import requests


def check_address(address):
    url = (
        f"https://api.mainnet.hiro.so/extended/v1/address/{address}/contracts"
        if os.environ.get("NETWORK") == "mainnet"
        else f"https://api.testnet.hiro.so/extended/v1/address/{address}/contracts"
    )
    print(f"Checking contracts for {address}...")
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        print(f"Total contracts: {data.get('total')}")
        for c in data.get("results", [])[:5]:
            print(f"- {c.get('contract_id')}")
    else:
        print(f"Error {res.status_code} for {address}")


check_address("ST1BK6TFDEJ4TBVWH5SHNB6SPNWGY06YZFG9WMM4P")
check_address("ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM")
