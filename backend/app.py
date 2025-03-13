# FacilitiPro API - Flask Backend

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for React frontend

# Configure Database (Supports SQLite & PostgreSQL)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///maintenance.db")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db = SQLAlchemy(app)


# --- DATABASE MODELS ---
class Area(db.Model):
    __tablename__ = "areas"
    area_id = db.Column(db.Integer, primary_key=True)
    area_name = db.Column(db.String(100), nullable=False, unique=True)


class Machine(db.Model):
    __tablename__ = "machines"
    machine_id = db.Column(db.Integer, primary_key=True)
    area_id = db.Column(db.Integer, db.ForeignKey("areas.area_id", ondelete="CASCADE"), nullable=False)
    machine_name = db.Column(db.String(100), nullable=False)
    asset_number = db.Column(db.String(50), unique=True, nullable=False)
    location = db.Column(db.String(255))
    last_maintenance_date = db.Column(db.String(50))  # Stored as string to avoid Date issues


class MaintenanceLog(db.Model):
    __tablename__ = "maintenance_logs"
    log_id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.Integer, db.ForeignKey("machines.machine_id", ondelete="CASCADE"), nullable=False)
    technician_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50), default=datetime.utcnow().strftime("%Y-%m-%d"))
    total_time_spent = db.Column(db.Float, nullable=False)
    comments = db.Column(db.Text)
    parts_used = db.Column(db.Text)  # JSON string to store parts data

# Ensure tables are created
with app.app_context():
    db.create_all()
    print("✅ Database tables initialized!")


# --- API ENDPOINTS ---
@app.route("/")
def home():
    return jsonify({"message": "Welcome to FacilitiPro API"})


# --- AREAS ---
@app.route("/areas", methods=["GET", "POST"])
def manage_areas():
    if request.method == "POST":
        data = request.get_json()
        if not data or "area_name" not in data:
            return jsonify({"error": "Missing 'area_name' field"}), 400

        new_area = Area(area_name=data["area_name"])
        db.session.add(new_area)
        db.session.commit()
        return jsonify({"message": "Area added!", "area_id": new_area.area_id}), 201

    areas = Area.query.all()
    return jsonify({"areas": [{"area_id": a.area_id, "area_name": a.area_name} for a in areas]})


# --- MACHINES ---
@app.route("/areas/<int:area_id>/machines", methods=["GET", "POST"])
def manage_machines(area_id):
    if request.method == "POST":
        data = request.get_json()
        if not data or "machine_name" not in data or "asset_number" not in data:
            return jsonify({"error": "Missing required fields"}), 400

        new_machine = Machine(
            area_id=area_id,
            machine_name=data["machine_name"],
            asset_number=data["asset_number"],
            location=data.get("location", ""),
            last_maintenance_date=data.get("last_maintenance_date", "")
        )
        db.session.add(new_machine)
        db.session.commit()
        return jsonify({"message": "Machine added!", "machine_id": new_machine.machine_id}), 201

    machines = Machine.query.filter_by(area_id=area_id).all()
    return jsonify({"machines": [{"machine_id": m.machine_id, "machine_name": m.machine_name, "asset_number": m.asset_number, "location": m.location, "last_maintenance_date": m.last_maintenance_date} for m in machines]})


# --- MAINTENANCE LOGS ---
@app.route("/machines/<int:machine_id>/maintenance", methods=["GET", "POST"])
def manage_maintenance(machine_id):
    if request.method == "POST":
        data = request.get_json()
        if not data or "technician_name" not in data or "total_time_spent" not in data:
            return jsonify({"error": "Missing required fields"}), 400

        new_log = MaintenanceLog(
            machine_id=machine_id,
            technician_name=data["technician_name"],
            total_time_spent=data["total_time_spent"],
            comments=data.get("comments", ""),
            parts_used=data.get("parts_used", "{}")  # Default empty JSON string
        )
        db.session.add(new_log)
        db.session.commit()
        return jsonify({"message": "Maintenance log added!", "log_id": new_log.log_id}), 201

    logs = MaintenanceLog.query.filter_by(machine_id=machine_id).all()
    return jsonify({"logs": [{"log_id": l.log_id, "technician_name": l.technician_name, "date": l.date, "total_time_spent": l.total_time_spent, "comments": l.comments, "parts_used": l.parts_used} for l in logs]})


# --- DELETE FUNCTIONS ---
@app.route("/areas/<int:area_id>", methods=["DELETE"])
def delete_area(area_id):
    area = Area.query.get_or_404(area_id)
    db.session.delete(area)
    db.session.commit()
    return jsonify({"message": "Area deleted successfully"})


@app.route("/machines/<int:machine_id>", methods=["DELETE"])
def delete_machine(machine_id):
    machine = Machine.query.get_or_404(machine_id)
    db.session.delete(machine)
    db.session.commit()
    return jsonify({"message": "Machine deleted successfully"})


@app.route("/maintenance/<int:log_id>", methods=["DELETE"])
def delete_maintenance(log_id):
    log = MaintenanceLog.query.get_or_404(log_id)
    db.session.delete(log)
    db.session.commit()
    return jsonify({"message": "Maintenance log deleted successfully"})


# --- RUN FLASK APP ---
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"🚀 Running FacilitiPro API on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port)
# Flask Backend Entry Point