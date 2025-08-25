import joblib
import pandas as pd
import os

def get_user_input(prompt, options=None):
    """A helper function to get validated user input."""
    while True:
        if options:
            print(f"\n{prompt}")
            for i, option in enumerate(options, 1):
                print(f"  {i}. {option}")
            choice = input(f"Enter your choice (1-{len(options)}): ")
            if choice.isdigit() and 1 <= int(choice) <= len(options):
                return options[int(choice) - 1]
            else:
                print("Invalid choice. Please enter a number from the list.")
        else:
            value = input(f"\n{prompt}: ")
            try:
                # Try to convert to a number (int or float)
                return float(value) if '.' in value else int(value)
            except ValueError:
                print("Invalid input. Please enter a numerical value.")

def run_prediction():
    """Main function to load the model and make a prediction based on user input."""
    model_path = 'final_model.joblib'
    preprocessor_path = 'preprocessor.joblib'

    # Check if the model files exist
    if not os.path.exists(model_path) or not os.path.exists(preprocessor_path):
        print("\nError: Model files not found!")
        print("Please run the 'server.py' simulation first to train and save the model.")
        return

    # 1. Load the saved model and preprocessor
    print("--- Loading Trained Heart Disease Model ---")
    model = joblib.load(model_path)
    preprocessor = joblib.load(preprocessor_path)
    print("Model loaded successfully.\n")

    # 2. Collect patient data from the user
    print("--- Please Enter Patient Details ---")
    patient_data = {}
    patient_data['age'] = get_user_input("Enter Age")
    patient_data['sex'] = get_user_input("Select Sex", ["Male", "Female"])
    patient_data['chest_pain_type'] = get_user_input("Select Chest Pain Type", ["Typical angina", "Atypical angina", "Non-anginal pain", "Asymptomatic"])
    patient_data['resting_blood_pressure'] = get_user_input("Enter Resting Blood Pressure (e.g., 120)")
    patient_data['cholestoral'] = get_user_input("Enter Cholestoral (e.g., 210)")
    patient_data['fasting_blood_sugar'] = get_user_input("Select Fasting Blood Sugar", ["Lower than 120 mg/ml", "Greater than 120 mg/ml"])
    patient_data['rest_ecg'] = get_user_input("Select Resting ECG Result", ["Normal", "ST-T wave abnormality", "Left ventricular hypertrophy"])
    patient_data['Max_heart_rate'] = get_user_input("Enter Max Heart Rate Achieved (e.g., 150)")
    patient_data['exercise_induced_angina'] = get_user_input("Exercise Induced Angina?", ["No", "Yes"])
    patient_data['oldpeak'] = get_user_input("Enter Oldpeak (e.g., 1.8)")
    patient_data['slope'] = get_user_input("Select Slope of the peak exercise ST segment", ["Upsloping", "Flat", "Downsloping"])
    patient_data['vessels_colored_by_flourosopy'] = get_user_input("Number of Major Vessels Colored by Flourosopy", ["Zero", "One", "Two", "Three"])
    patient_data['thalassemia'] = get_user_input("Select Thalassemia Type", ["Normal", "Fixed Defect", "Reversable Defect"])

    # 3. Create a DataFrame and preprocess the data
    df = pd.DataFrame([patient_data])
    processed_data = preprocessor.transform(df)

    # 4. Make the prediction
    prediction = model.predict(processed_data)
    probability = model.predict_proba(processed_data)
    prediction_result = prediction[0]
    risk_probability = probability[0][1] * 100

    # 5. Display the result
    print("\n" + "="*30)
    print("   PREDICTION RESULT")
    print("="*30)
    if prediction_result == 1:
        print("\nPrediction: 1 - Heart Disease LIKELY")
    else:
        print("\nPrediction: 0 - Heart Disease UNLIKELY")
    
    print(f"Confidence (Risk Probability): {risk_probability:.2f}%")
    print("="*30)

if __name__ == '__main__':
    run_prediction()