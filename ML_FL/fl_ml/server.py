import flwr as fl
from flwr.common import Metrics, Parameters
from typing import List, Tuple, Optional
import numpy as np
import joblib
import pandas as pd

# Import local modules
from .client import HeartDiseaseClient
from .logging_utils import initialize_log
from .utils import load_data  # Corrected from 'utils' to 'util' to match your filename
from .model import get_model

# This custom strategy's only job is to capture the final aggregated parameters
class SaveModelStrategy(fl.server.strategy.FedAvg):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.final_model_parameters: Optional[Parameters] = None

    def aggregate_fit(
        self,
        server_round: int,
        results: List[Tuple[fl.server.client_proxy.ClientProxy, fl.common.FitRes]],
        failures: List[Tuple[fl.server.client_proxy.ClientProxy, fl.common.FitRes]],
    ) -> Tuple[Optional[Parameters], dict]:
        
        # Call the parent class's aggregate_fit to do the real averaging
        aggregated_parameters, aggregated_metrics = super().aggregate_fit(server_round, results, failures)
        
        # Save the latest aggregated parameters
        if aggregated_parameters is not None:
            self.final_model_parameters = aggregated_parameters
            
        return aggregated_parameters, aggregated_metrics

# --- Helper Functions ---
def weighted_average(metrics: List[Tuple[int, Metrics]]) -> Metrics:
    total_examples = sum([num_examples for num_examples, _ in metrics])
    accuracy = sum([num_examples * m["accuracy"] for num_examples, m in metrics]) / total_examples
    return {"accuracy": accuracy}

# FIX: Removed the unnecessary int() conversion. Pass the client ID as a string.
def client_fn(cid: str) -> HeartDiseaseClient:
    return HeartDiseaseClient(cid)

def fit_config(server_round: int):
    return {"server_round": server_round}

# --- Main Execution Block ---
if __name__ == "__main__":
    initialize_log()
    print("Starting Federated Learning Simulation...")

    # Use our new custom strategy that saves the model
    strategy = SaveModelStrategy(
        fraction_fit=1.0,
        fraction_evaluate=1.0,
        min_fit_clients=3,
        min_evaluate_clients=3,
        min_available_clients=3,
        evaluate_metrics_aggregation_fn=weighted_average,
        on_fit_config_fn=fit_config,
    )

    # Start the simulation
    fl.simulation.start_simulation(
        client_fn=client_fn,
        num_clients=3,
        config=fl.server.ServerConfig(num_rounds=10),
        strategy=strategy,
    )
    print("Simulation finished.")

    print("\nSaving the final global model and data preprocessor...")
    # Get the final parameters from our custom strategy
    final_parameters = strategy.final_model_parameters
    
    if final_parameters is not None:
        _, preprocessor = load_data()
        
        # Convert parameters back to NumPy arrays
        final_weights = fl.common.parameters_to_ndarrays(final_parameters)
        
        num_features = final_weights[0].shape[1]
        
        final_model = get_model(num_features)
        
        final_model.coef_ = final_weights[0]
        final_model.intercept_ = final_weights[1]
        final_model.classes_ = np.array([0, 1])

        joblib.dump(final_model, 'final_model.joblib')
        joblib.dump(preprocessor, 'preprocessor.joblib')
        
        print("Model and preprocessor saved successfully!")
    else:
        print("Error: Could not save the model because the final parameters were not available.")