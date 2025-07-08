import joblib
import os
import pandas as pd

MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'model')

models = {}
encoders = {}
for cancer in ['breast', 'cervical', 'colorectal']:
    try:
        model_path = os.path.join(MODEL_DIR, f"risk_model_{cancer}.pkl")
        encoder_path = os.path.join(MODEL_DIR, f"label_encoder_{cancer}.pkl")
        models[cancer] = joblib.load(model_path)
        encoders[cancer] = joblib.load(encoder_path)
    except FileNotFoundError:
        print(f"Model or encoder not found for {cancer}")

def extract_features(row):
    return [
        int(row['age']),
        int(row['smoking']),
        int(row['family_history']),
        int(row.get('alcohol', 0)),
        int(row.get('exercise', 1)),
        float(row.get('bmi', 25))
    ]

def predict_risk(row):
    results = {}
    features = extract_features(row)
    FEATURE_COLS = ["age", "smoking", "family_history", "alcohol", "exercise", "bmi"]
    X = pd.DataFrame([features], columns=FEATURE_COLS)

    if row['gender'] == 'F':
        if models.get('breast'):
            pred = models['breast'].predict(X)[0]
            results['breast'] = encoders['breast'].inverse_transform([pred])[0]
        if models.get('cervical'):
            pred = models['cervical'].predict(X)[0]
            results['cervical'] = encoders['cervical'].inverse_transform([pred])[0]
    
    if models.get('colorectal'):
        pred = models['colorectal'].predict(X)[0]
        results['colorectal'] = encoders['colorectal'].inverse_transform([pred])[0]

    return results