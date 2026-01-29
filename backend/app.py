import os
import joblib
import numpy as np
from flask import Flask, jsonify
from flask_pymongo import PyMongo
from config import MONGO_URI

app = Flask(__name__)

# ---------------- MongoDB ----------------
app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)

# ---------------- Load AI Model ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "..",
    "ai_module",
    "models",
    "risk_prediction_model.pkl"
)

model = joblib.load(MODEL_PATH)
print("AI model loaded successfully")

# ---------------- Routes ----------------
@app.route("/")
def home():
    return "Backend is running successfully"

@app.route("/predict-risk")
def predict_risk():

    sample_data = [[
        2,    # fitting_type
        72,   # age_months
        180,  # last_inspection_gap_days
        15,   # inspection_count
        6,    # previous_defect_count
        2,    # environment
        2,    # load_category
        2     # current_condition
    ]]

    proba = model.predict_proba(sample_data)[0]

    return jsonify({
        "Low": round(float(proba[0]), 3),
        "Medium": round(float(proba[1]), 3),
        "High": round(float(proba[2]), 3),
        "Final": ["Low", "Medium", "High"][int(proba.argmax())]
    })

# ---------------- START SERVER ----------------
if __name__ == "__main__":
    print("Flask server starting on port 5000...")
    app.run(host="127.0.0.1", port=5000, debug=True)
