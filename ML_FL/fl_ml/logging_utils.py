import csv
import os
import numpy as np
from filelock import FileLock

LOG_FILE = 'simulation_log.csv'
LOCK_FILE = LOG_FILE + '.lock'

def initialize_log():
    """Creates a fresh CSV file with headers, safely."""
    with FileLock(LOCK_FILE):
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
        with open(LOG_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Round', 'ClientID', 'Stage', 'Parameter_Representation'])
            f.flush()

def log_parameters(round_num, client_id, stage, parameters):
    """Logs a representation of the parameters to the CSV file, using a lock."""
    representation = ""
    try:
        if stage.lower() == 'encrypted' and isinstance(parameters, (bytes, bytearray)):
            representation = parameters[:16].hex() + '...'
        elif isinstance(parameters, list) and all(isinstance(p, np.ndarray) for p in parameters):
            param_sum = sum(np.sum(p) for p in parameters[:2])
            representation = f'{param_sum:.4f}'
        elif isinstance(parameters, np.ndarray):
            representation = f'{np.sum(parameters):.4f}'
        else:
            representation = str(parameters)
    except Exception as e:
        representation = f"Error processing parameters: {e}"

    with FileLock(LOCK_FILE):
        with open(LOG_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([round_num, client_id, stage, representation])
            f.flush()
            os.fsync(f.fileno())