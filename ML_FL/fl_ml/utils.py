import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def load_data(num_clients=3):
    """Loads your specific Heart Disease dataset, preprocesses it, and partitions it."""
    
    script_location = Path(__file__).resolve().parent
    path = script_location.parent / 'data' / 'heart.csv'
    
    df = pd.read_csv(path)

    # Defines categorical and numerical features based on YOUR file
    categorical_features = [
        'sex', 
        'chest_pain_type', 
        'fasting_blood_sugar', 
        'rest_ecg', 
        'exercise_induced_angina', 
        'slope', 
        'vessels_colored_by_flourosopy', 
        'thalassemia'
    ]
    numerical_features = [
        'age', 
        'resting_blood_pressure', 
        'cholestoral', 
        'Max_heart_rate', 
        'oldpeak'
    ]
    
    numeric_transformer = Pipeline(steps=[('scaler', StandardScaler())])
    categorical_transformer = Pipeline(steps=[('onehot', OneHotEncoder(handle_unknown='ignore'))])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numerical_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    X = df.drop('target', axis=1)
    y = df['target']
    
    X_processed = preprocessor.fit_transform(X)

    total_samples = X_processed.shape[0]
    indices = np.random.permutation(total_samples)
    partition_size = total_samples // num_clients
    
    client_data = []
    for i in range(num_clients):
        start = i * partition_size
        end = (i + 1) * partition_size if i < num_clients - 1 else total_samples
        client_indices = indices[start:end]
        
        X_client = X_processed[client_indices]
        y_client = y.iloc[client_indices].values
        
        X_train, X_test, y_train, y_test = train_test_split(
            X_client, y_client, test_size=0.2, random_state=42
        )
        client_data.append(((X_train, y_train), (X_test, y_test)))
        
    return client_data, preprocessor