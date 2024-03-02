from solcx import compile_standard
import json
import os
from web3 import Web3
from dotenv import load_dotenv


load_dotenv()


with open("SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Compile Our Solidity
compiled_sol = compile_standard({
        "language": "Solidity",
        "sources": {
            "SimpleStorage.sol": {
                "content": simple_storage_file
            }
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        }
    },
    solc_version="0.6.0"
)

# Save compiled contract into a json
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# Get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

# Get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# For connecting to sepolia
w3 = Web3(Web3.HTTPProvider("https://sepolia.infura.io/v3/7b991e7711b3474fa982692efb6329aa"))
chain_id = 11155111
my_address = "0xD21da6ACD65bf0BeeC3d3BF10BC236B88Fd7CDC4"
private_key = os.getenv("PRIVATE_KEY")

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get the latests transaction
nonce = w3.eth.get_transaction_count(my_address)
print("Nonce is: {}".format(nonce))
# 1. Build a transaction
print("Building contract...")
transaction = SimpleStorage.constructor().build_transaction({"chainId": chain_id, "from": my_address, "nonce": nonce})
# 2. Sign a transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
# 3. Send a transaction
print("Deploying contract...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)


# Working with the contract, you always need
# Contract Address
# Contract ABI
print("Retrieving contract...")
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# Call -> Simulate making the call and getting a return value
# Trasanct -> Actually make a state change

# Initial value of favorite number
print("Favorite number is: {}".format(simple_storage.functions.retrieve().call()))

print("Updating contract...")
store_transaction = simple_storage.functions.store(15).build_transaction({
    "chainId": chain_id,
    "from": my_address,
    "nonce": nonce + 1
})
signed_store_tx = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)
send_store_tx = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)
send_store_tx_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash=send_store_tx)
print("Favorite number again is: {}".format(simple_storage.functions.retrieve().call()))
