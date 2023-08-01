import pandas as pd
from web3 import Web3

infura_endpoint = 'https://mainnet.infura.io/v3/61e61029da4c420999f04caea8f65a46'

start_block = 1000000
end_block = 1001000

def is_contract(web3, address):
    code = web3.eth.get_code(address).hex()
    return len(code) > 2  # If code exists, it is a contract

def get_unique_contract_accounts_with_gas_consumption(start_block, end_block):
    web3 = Web3(Web3.HTTPProvider(infura_endpoint))

    contract_gas_consumption = {}
    for block_number in range(start_block, end_block + 1):
        block = web3.eth.get_block(block_number)
        for transaction_hash in block['transactions']:
            transaction = web3.eth.get_transaction(transaction_hash)

            sender = transaction['from']
            receiver = transaction['to']

            if is_contract(web3, sender):
                contract_gas_consumption[sender] = contract_gas_consumption.get(sender, 0) + transaction['gas']

            if receiver and is_contract(web3, receiver):
                contract_gas_consumption[receiver] = contract_gas_consumption.get(receiver, 0) + transaction['gas']

            if transaction.get('creates') and is_contract(web3, transaction['creates']):
                contract_gas_consumption[transaction['creates']] = contract_gas_consumption.get(transaction['creates'], 0) + transaction['gas']

    unique_contract_accounts = list(contract_gas_consumption.keys())
    gas_consumption_list = list(contract_gas_consumption.values())

    return unique_contract_accounts, gas_consumption_list

unique_contract_accounts, gas_consumption_list = get_unique_contract_accounts_with_gas_consumption(start_block, end_block)

df = pd.DataFrame({
    "Contract Accounts": unique_contract_accounts,
    "Gas Consumption": gas_consumption_list
})

df.to_excel("contract_accounts_with_gas_consumption.xlsx", index=False)

print("Excel file created successfully.")
