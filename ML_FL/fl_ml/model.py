from sklearn.linear_model import LogisticRegression

def get_model(num_features):
    """Creates a scikit-learn Logistic Regression model."""
    model = LogisticRegression(
        C=1.0,
        max_iter=2000,
        random_state=42,
        solver='liblinear'
    )
    return model