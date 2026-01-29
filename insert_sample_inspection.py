from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["railway_track"]

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

db.inspections.insert_one(inspection)

print("Sample inspection data inserted successfully")
