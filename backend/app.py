import os
import joblib
import numpy as np
from flask import Flask, jsonify
from flask_pymongo import PyMongo
from config import MONGO_URI

# ---------------- Flask App ----------------
app = Flask(__name__)

# ---------------- MongoDB Config ----------------
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

# ---------------- Encoding Maps (same as training logic) ----------------
FITTING_TYPE_MAP = {
    "Elastic Rail Clip": 0,
    "Rail Pad": 1,
    "Liner": 2
}

ENV_MAP = {
    "rural": 0,
    "urban": 1,
    "coastal": 2
}

LOAD_MAP = {
    "low": 0,
    "medium": 1,
    "high": 2
}

COND_MAP = {
    "good": 0,
    "minor": 1,
    "major": 2
}

# ---------------- Routes ----------------
@app.route("/")
def home():
    return "Backend is running successfully"

@app.route("/test-db")
def test_db():
    mongo.db.test.insert_one({"status": "connected"})
    return "MongoDB Connected Successfully"

# -------- Dynamic AI Prediction from MongoDB --------
@app.route("/predict-risk/<fitting_id>")
def predict_risk(fitting_id):

    # Fetch latest inspection for the fitting
    inspection = mongo.db.inspections.find_one(
        {"fitting_id": fitting_id},
        sort=[("date", -1)]
    )

    if not inspection:
        return jsonify({"error": "No inspection data found"}), 404

    # Build feature vector (ORDER MUST MATCH TRAINING)
    sample_data = [[
        FITTING_TYPE_MAP.get(inspection.get("fitting_type"), 0),
        int(inspection.get("age_months", 0)),
        int(inspection.get("last_inspection_gap_days", 0)),
        int(inspection.get("inspection_count", 0)),
        int(inspection.get("previous_defect_count", 0)),
        ENV_MAP.get(inspection.get("environment"), 0),
        LOAD_MAP.get(inspection.get("load_category"), 0),
        COND_MAP.get(inspection.get("current_condition"), 0)
    ]]

    # AI prediction (probabilities)
    proba = model.predict_proba(sample_data)[0]

    result = {
        "Low": round(float(proba[0]), 3),
        "Medium": round(float(proba[1]), 3),
        "High": round(float(proba[2]), 3),
        "Final_Risk": ["Low", "Medium", "High"][int(proba.argmax())]
    }

    # Store prediction in MongoDB
    mongo.db.predictions.insert_one({
        "fitting_id": fitting_id,
        "prediction": result
    })

    return jsonify(result)



#--------------------------------------------------

@app.route("/add-sample-inspection")
def add_sample_inspection():

    inspection = {
        "fitting_id": "FIT_001",
        "fitting_type": "Elastic Rail Clip",
        "age_months": 60,
        "last_inspection_gap_days": 120,
        "inspection_count": 10,
        "previous_defect_count": 4,
        "environment": "coastal",
        "load_category": "high",
        "current_condition": "major",
        "date": "2026-01-20"
    }


# ---------------- Run Server ----------------
if __name__ == "__main__":
    print("Flask server starting on port 5000...")
    app.run(host="127.0.0.1", port=5000, debug=True)
