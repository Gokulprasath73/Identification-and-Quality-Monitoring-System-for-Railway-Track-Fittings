print("DATASET SCRIPT STARTED")

import pandas as pd
import random

# Number of records
NUM_RECORDS = 500

fitting_types = ["Elastic Rail Clip", "Rail Pad", "Liner"]
environments = ["urban", "rural", "coastal"]
load_categories = ["low", "medium", "high"]
conditions = ["good", "minor", "major"]

data = []

for i in range(1, NUM_RECORDS + 1):
    fitting_id = f"FIT_{i:04d}"
    fitting_type = random.choice(fitting_types)
    age_months = random.randint(6, 72)
    last_inspection_gap_days = random.randint(15, 120)
    inspection_count = random.randint(1, 15)
    previous_defect_count = random.randint(0, 6)
    environment = random.choice(environments)
    load_category = random.choice(load_categories)
    current_condition = random.choice(conditions)

    # ---- Risk logic (IMPORTANT) ----
    if (
        age_months > 48
        or previous_defect_count >= 4
        or current_condition == "major"
        or (environment == "coastal" and load_category == "high")
    ):
        risk_level = "High"
    elif (
        age_months > 24
        or previous_defect_count >= 2
        or current_condition == "minor"
    ):
        risk_level = "Medium"
    else:
        risk_level = "Low"

    data.append([
        fitting_id,
        fitting_type,
        age_months,
        last_inspection_gap_days,
        inspection_count,
        previous_defect_count,
        environment,
        load_category,
        current_condition,
        risk_level
    ])

# Create DataFrame
columns = [
    "fitting_id",
    "fitting_type",
    "age_months",
    "last_inspection_gap_days",
    "inspection_count",
    "previous_defect_count",
    "environment",
    "load_category",
    "current_condition",
    "risk_level"
]

df = pd.DataFrame(data, columns=columns)

# Save to CSV
df.to_csv("track_fitting_inspection_data.csv", index=False)

print("Dataset generated successfully with", NUM_RECORDS, "records")

print("DATASET SCRIPT FINISHED")
