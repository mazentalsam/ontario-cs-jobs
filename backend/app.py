from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)


# -----------------------------
# DATABASE CONNECTION
# -----------------------------
def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), "..", "database", "jobs.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# TEST ENDPOINT
# -----------------------------
@app.get("/")
def home():
    return jsonify({"message": "Ontario CS Jobs API is running!"})

# -----------------------------
# FETCH JOBS ENDPOINT
# -----------------------------
@app.get("/jobs")
def get_jobs():
    conn = get_db_connection()
    c = conn.cursor()

    # Query parameters
    company = request.args.get("company")
    location = request.args.get("location")
    search = request.args.get("search")
    limit = request.args.get("limit")
    category = request.args.get("category")  # internship, new grad, co-op (optional future field)

    # Base query
    query = "SELECT * FROM jobs WHERE 1=1"
    params = []

    # Dynamic filtering
    if company:
        query += " AND company LIKE ?"
        params.append(f"%{company}%")

    if location:
        query += " AND location LIKE ?"
        params.append(f"%{location}%")

    if search:
        query += " AND title LIKE ?"
        params.append(f"%{search}%")

    # Optional limit
    if limit:
        query += " LIMIT ?"
        params.append(limit)

    rows = c.execute(query, params).fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows])


# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
