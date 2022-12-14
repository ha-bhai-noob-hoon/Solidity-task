from web3 import Web3
from solcx import compile_standard, install_solc
import json

with open('./simplestorage.sol', 'r') as file:
    simple_storage_file = file.read()


install_solc("0.6.0")
    
# Compile our Solidity

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0"
    
)
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# for connecting to ganache
w3 = Web3(Web3.HTTPProvider('https://rinkeby.infura.io/v3/dcf9cbc214d647609811ed4e096ed398'))
chain_id = 4
my_address = "0xA8E373f59903f157A6c19289B0da7fCEC294581c"
private_key = "0x31c4fcacf1b110704d1c46959efdd2adf51f193b63e221ef74e02491cdb6bef6"



# create the contract in python
SimpleStorage = w3.eth.contract(abi = abi, bytecode = bytecode)
# get latest transaction
nonce = w3.eth.getTransactionCount(my_address)


# build a transaction
# sign a transaction
# send a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce
    }
)
signed_txn = w3.eth.account.sign_transaction(transaction, private_key = private_key)
# send this signed transaction 
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Working with contract, you need
# Contract ABI
# Contract address
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi = abi)

print(simple_storage.functions.retrieve().call())
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,

    }
)
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key = private_key
)
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print(simple_storage.functions.retrieve().call())