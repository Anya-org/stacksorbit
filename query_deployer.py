import os
import requests

def search_contract(name):
    url = f"https://api.mainnet.hiro.so/extended/v1/search?id={name}" if os.environ.get('NETWORK') == 'mainnet' else f"https://api.testnet.hiro.so/extended/v1/search?id={name}"
    print(f"Searching for {name} on testnet...")
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        if data.get('found'):
            result = data.get('result', {})
            entity_type = result.get('entity_type')
            
            # The search API might return a transaction or a contract
            if entity_type == 'smart_contract':
                contract_data = result.get('smart_contract', {})
                contract_id = contract_data.get('contract_id', '')
                print(f"Found active deployment: {contract_id}")
            elif entity_type == 'tx':
                tx_data = result.get('tx', {})
                tx_type = tx_data.get('tx_type')
                if tx_type == 'smart_contract':
                    sc_data = tx_data.get('smart_contract', {})
                    contract_id = sc_data.get('contract_id', '')
                    sender = tx_data.get('sender_address', '')
                    print(f"Found deployment TX. Deployer: {sender}, Contract: {contract_id}")
    else:
        print(f"Error querying {name}: {res.status_code}")

if __name__ == "__main__":
    search_contract("conxian-protocol")
    search_contract("ops-engine")
    search_contract("bme-engine")
    search_contract("cxd-token")
