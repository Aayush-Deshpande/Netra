from sklearn.linear_model import LogisticRegression

def train(model: LogisticRegression, X_train, y_train):
    """Train the model on the provided data."""
    model.fit(X_train, y_train)
    return model, len(X_train)

def test(model: LogisticRegression, X_test, y_test):
    """Test the model's performance."""
    accuracy = model.score(X_test, y_test)
    return len(X_test), {"accuracy": accuracy}