from flask import Flask
from flask_pymongo import PyMongo
from config import MONGO_URI

app = Flask(__name__)

# MongoDB config
app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)


@app.route("/")

def home():
    return "Backend is running successfully"

@app.route("/test-db")
def test_db():
    mongo.db.test.insert_one({"status": "connected"})
    return "MongoDB Connected Successfully"

if __name__ == "__main__":
    app.run(debug=True)
