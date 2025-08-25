from web3 import Web3
import json

# --- Configuration ---
GANACHE_URL = "http://127.0.0.1:7545"

# --- Details from your Hardhat Deployment ---
CONTRACT_ADDRESS = "0xb8e563b95b9d8202C9f886C326854588d71D863a"
path_to_artifact_string = r"E:\kurukshetra\hardhat-audit\artifacts\contracts\AuditTrail.sol\AuditTrail.json"

# --- Accounts to register (from client.py) ---
ganache_accounts_to_register = [
    "0x4A9591B4c5E931C7fAc4A5ef58E55148963b685e",
    "0xddbFE1B6D62F2AA5249Cf52607fCcc9764cB0A82",
    "0xf0fd208E5e5258b71dFb4C88beB9e9caa654CBef",
]

# --- Owner's account (the one that deployed the contract) ---
# Replace with the actual owner's address and private key from Ganache
OWNER_ACCOUNT_ADDRESS = "0xE11c3cCa938EF41bc1a3cF1A78Dc4aDe6FbbdCF3"  # <-- Paste the owner's address here
OWNER_PRIVATE_KEY = "0x65da7c9f00df230528b5007511ba3097805dbfdf3c2d1a7fcdd9e2472338bba0"      # <-- Paste the owner's private key here


try:
    with open(path_to_artifact_string, 'r') as f:
        artifact = json.load(f)
        CONTRACT_ABI = artifact['abi']
except Exception as e:
    print("\n\nERROR: Could not load the Hardhat artifact file.")
    print(f"Please check that the path is correct: {path_to_artifact_string}\n\n")
    raise e

# Connect to the Ganache blockchain
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
if not w3.is_connected():
    raise ConnectionError("Failed to connect to Ganache blockchain.")

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
nonce = w3.eth.get_transaction_count(OWNER_ACCOUNT_ADDRESS)

print("Starting registration of hospital accounts...")

for account_address in ganache_accounts_to_register:
    print(f"Registering hospital: {account_address}...")
    try:
        # Build the transaction to call the 'registerHospital' function
        tx = contract.functions.registerHospital(account_address).build_transaction({
            'from': OWNER_ACCOUNT_ADDRESS,
            'nonce': nonce,
        })

        # Sign and send the transaction
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=OWNER_PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        # Wait for the transaction to be mined
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        if receipt.status == 1:
            print(f"✅ Successfully registered {account_address}. Transaction hash: {tx_hash.hex()}")
        else:
            print(f"❌ Failed to register {account_address}. Transaction reverted.")
        
        # Increment nonce for the next transaction
        nonce += 1
        
    except Exception as e:
        print(f"❌ Error during registration for {account_address}: {e}")

print("Registration process complete.")