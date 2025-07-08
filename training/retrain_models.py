import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("data/synthetic_risk_data.csv")

feature_cols = ["age", "smoking", "family_history", "alcohol", "exercise", "bmi"]

for col in ["smoking", "family_history", "alcohol", "exercise"]:
    df[col] = df[col].astype(int)

output_dir = "model"
os.makedirs(output_dir, exist_ok=True)

cancer_map = {
    "breast": "breast_cancer_risk",
    "cervical": "cervical_cancer_risk",
    "colorectal": "colorectal_cancer_risk"
}

for cancer, label_col in cancer_map.items():
    print(f"Training model for {cancer} cancer...")

    subset = df[df[label_col].notna() & (df[label_col] != "")].copy()

    if subset.empty:
        print(f"!! Skipping {cancer} cancer due to no data.")
        continue

    le = LabelEncoder()
    y = le.fit_transform(subset[label_col])
    X = subset[feature_cols]

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    model_path = os.path.join(output_dir, f"risk_model_{cancer}.pkl")
    encoder_path = os.path.join(output_dir, f"label_encoder_{cancer}.pkl")
    joblib.dump(model, model_path)
    joblib.dump(le, encoder_path)

    print(f"Saved {model_path} and {encoder_path}")

print("All models trained and saved.")