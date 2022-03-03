from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Compile our Solidity

print("installing...")
install_solc("0.6.0")
compile_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)


with open("compiled_code.json", "w") as file:
    json.dump(compile_sol, file)

# get bytecode
bytecode = compile_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compile_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# ganache is simulated env
# for connecting to ganache

# w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))
# chain_id = 1337
# my_address = "0xd188C04bcDeF19B009EfdE63736b358D6B10f870"
# private_key = os.getenv("PRIVATE_KEY")
# print(private_key)

# rinkeby (infura)
w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/34b38db54c5c4f5a806ccb646174cfab")
)
chain_id = 4
my_address = "0x64e4c119b09f618C4031EE34AA8A8ba10F299A26"
private_key = os.getenv("PRIVATE_KEY_METAMASK")
print(private_key)


# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
# Build transaction
# Sign transaction
# Send transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
        "gasPrice": w3.eth.gas_price,
    }
)

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

print("deploying contract...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("deployed!")

# Working with the contract, you always need
# Contract Address
# Contract ABI
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Call -> Simulate making the call and geting the return value
# Transact -> Actually make a state change

#  Initial value of favorite number
print(simple_storage.functions.retrieve().call())
print("updating contract...")

store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "gasPrice": w3.eth.gas_price,
        "nonce": nonce + 1,
    }
)

signed_store_tx = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)

send_store_tx = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("updated!")
print(simple_storage.functions.retrieve().call())
