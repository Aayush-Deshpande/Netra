import flwr as fl
import numpy as np
import sys
import os

# Add the project's root directory to the Python path
# Note: This line is not strictly necessary if you run the server as a module (`python -m ...`)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from ML_FL.fl_ml.utils import load_data
from ML_FL.fl_ml.model import get_model
from ML_FL.fl_ml.train import train, test
from ML_FL.fl_ml.logging_utils import log_parameters
from ML_FL.fl_ml.blockchain_utils import log_update_to_blockchain


# --- Configuration ---
CLIENT_DATASETS, _ = load_data(num_clients=3)
NOISE_MULTIPLIER = 0.5


# --- Flower Client Definition ---
class HeartDiseaseClient(fl.client.NumPyClient):
    """Defines a federated learning client for a hospital node."""

    # FIX: The constructor method name is now corrected to __init__
    def __init__(self, client_id: str):
        self.client_id = client_id
        (self.X_train, self.y_train), (self.X_test, self.y_test) = CLIENT_DATASETS[int(self.client_id)]
        
        num_features = self.X_train.shape[1]
        self.model = get_model(num_features)

        # Perform an initial training to create the model's attributes
        train(self.model, self.X_train, self.y_train)

    def get_parameters(self, config):
        """Returns the model's parameters (weights)."""
        return [self.model.coef_, self.model.intercept_]

    def set_parameters(self, parameters):
        """Sets the model's parameters received from the server."""
        self.model.coef_ = parameters[0]
        self.model.intercept_ = parameters[1]

    def fit(self, parameters, config):
        """Trains the model, adds noise, and logs a hash to the blockchain."""
        current_round = config.get("server_round", 0)
        
        self.set_parameters(parameters)
        self.model, num_samples = train(self.model, self.X_train, self.y_train)
        
        original_weights = self.get_parameters(config={})
        log_parameters(current_round, self.client_id, 'Original_Weights', original_weights)

        coef_noise = np.random.normal(0, NOISE_MULTIPLIER, original_weights[0].shape)
        intercept_noise = np.random.normal(0, NOISE_MULTIPLIER, original_weights[1].shape)
        noisy_weights = [original_weights[0] + coef_noise, original_weights[1] + intercept_noise]
        log_parameters(current_round, self.client_id, 'Noisy_Weights', noisy_weights)
        
        # Using the credentials you provided
        ganache_accounts = [
            ("0x93C77E9573a8b6a1a206E0Ded2cbF76832ac0B65", "0x97f191501e4bbd7284e7390f74550994c673af16547b0524d96125506c369356"),
            ("0x09C015194c1231dE307a3963Cdfe73B7cAAd9787", "0x5e78e952ea80061c02b3636817a296e770de82eae0424cbc7002677c2a75e7dc"),
            ("0x4A9591B4c5E931C7fAc4A5ef58E55148963b685e", "0x374fe1796dcfd59cef93214ac1bbc4d22e3d695945d9ca45d7d6bf9a216d63b3"),
        ]

        account_address, private_key = ganache_accounts[int(self.client_id)]
        log_update_to_blockchain(current_round, noisy_weights, account_address, private_key)
        
        return noisy_weights, num_samples, {}

    def evaluate(self, parameters, config):
        """Evaluates the model on the local test dataset."""
        self.set_parameters(parameters)
        num_samples, metrics = test(self.model, self.X_test, self.y_test)
        loss = 1.0 - metrics["accuracy"]
        return loss, num_samples, metrics