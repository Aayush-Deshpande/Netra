from web3 import Web3
import hashlib
import json

# --- Configuration ---
GANACHE_URL = "http://127.0.0.1:7545"

# --- Details from your Hardhat Deployment ---
# !! IMPORTANT !!
# 1. Update this with YOUR unique contract address after deployment
CONTRACT_ADDRESS = "0xE7261cd2c0F898623e78d52a97BB275A2556d78e" # <-- REPLACE WITH YOURS

# 2. Update this with the corrected absolute path to YOUR Hardhat artifact file
path_to_artifact_string = r"E:\kurukshetra\hardhat-audit\artifacts\contracts\AuditTrail.sol\AuditTrail.json" # <-- REPLACE WITH YOURS
# --------------------------------------------------------------------

try:
    with open(path_to_artifact_string, 'r') as f:
        artifact = json.load(f)
        CONTRACT_ABI = artifact['abi']
except Exception as e:
    print("\n\nERROR: Could not load the Hardhat artifact file.")
    print(f"Please check that the path is correct in blockchain_utils.py: {path_to_artifact_string}\n\n")
    raise e

# Connect to the Ganache blockchain
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
if not w3.is_connected():
    raise ConnectionError("Failed to connect to Ganache blockchain.")

# Create a contract object that Python can interact with
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

def hash_weights(weights: list) -> bytes:
    """Creates a unique SHA-256 hash of the model weights."""
    weight_str = str([arr.tolist() for arr in weights])
    return hashlib.sha256(weight_str.encode()).digest()

def log_update_to_blockchain(round_num: int, weights: list, client_account: str, client_private_key: str):
    """Builds, signs, and sends a transaction to the smart contract."""
    try:
        update_hash = hash_weights(weights)

        tx = contract.functions.recordUpdate(round_num, update_hash).build_transaction({
            'from': client_account,
            'nonce': w3.eth.get_transaction_count(client_account),
        })

        signed_tx = w3.eth.account.sign_transaction(tx, private_key=client_private_key)

        # Send the transaction to the blockchain
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

        # --------------------------------------------------------------------
        # ADDED: Wait for the transaction to be mined and get the receipt
        print(f"  [Blockchain] Waiting for transaction receipt for Tx: {tx_hash.hex()}")
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        # Check if the transaction was successful (status == 1)
        if tx_receipt.status == 1:
            print(f"  [Blockchain] Transaction for client {client_account[:10]}... confirmed successfully!")
        else:
            print(f"  [Blockchain] Error: Transaction for client {client_account[:10]}... failed on the blockchain.")
        # --------------------------------------------------------------------

    except Exception as e:
        print(f"  [Blockchain] Error logging to blockchain: {e}")