import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

print("Training started...")

# Load dataset
df = pd.read_csv("data/track_fitting_inspection_data.csv")
print("Dataset loaded")

# Encode categorical columns
encoder = LabelEncoder()
categorical_cols = [
    "fitting_type",
    "environment",
    "load_category",
    "current_condition",
    "risk_level"
]

for col in categorical_cols:
    df[col] = encoder.fit_transform(df[col])


# Drop non-numeric / ID column
df = df.drop("fitting_id", axis=1)

# Features & target
X = df.drop("risk_level", axis=1)
y = df["risk_level"]


# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)
model.fit(X_train, y_train)

print("Model training completed")

# Accuracy
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Model accuracy:", accuracy)

# Save model
os.makedirs("ai_module/models", exist_ok=True)
joblib.dump(model, "ai_module/models/risk_prediction_model.pkl")

print("Model saved successfully")
