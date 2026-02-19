from flask import Blueprint, request, jsonify
from models.models import User, Doctor, Patient, Appointment, Department, Availability, Treatment, db
from werkzeug.security import generate_password_hash
from utils.admin_required import admin_required
from flask_jwt_extended import jwt_required, get_jwt
from tasks.daily_reminder import send_daily_reminders
from cache import cache

admin_bp = Blueprint('admin', __name__, url_prefix='api/admin')

@admin_bp.route('/dashboard', methods=['GET'])
@admin_required
def dashboard():
    return {
        "total_doctors": Doctor.query.count(),
        "total_patients": Patient.query.count(),
        "total_appointments": Appointment.query.count()
    }, 200

@admin_bp.route('/doctor', methods=['POST'])
@admin_required
def add_doctor():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    department_id = data.get("department_id")
    specialization = data.get("specialization")
    experience_years = data.get("experience_years", 0)

    if not username or not password or not email or not department_id or not specialization:
        return {"message": "Missing required fields"}, 400

    if User.query.filter_by(username=username).first():
        return {"message": "Username already exists"}, 409

    if User.query.filter_by(email=email).first():
        return {"message": "Email already exists"}, 409

    user = User(
        username=username,
        email=email,
        password=generate_password_hash(password),
        role="doctor"
    )
    db.session.add(user)
    db.session.commit()

    doctor = Doctor(
        user_id=user.id,
        department_id=department_id,
        specialization=specialization,
        experience_years=experience_years
    )
    db.session.add(doctor)
    db.session.commit()

    return {"message": "Doctor added successfully"}, 201

@admin_bp.route('/doctors', methods=['GET'])
@jwt_required()
def get_doctors():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return {"message": "Admin access required"}, 403

    specialization = request.args.get("specialization")

    query = Doctor.query.join(User)

    if specialization:
        query = query.filter(
            Doctor.specialization.ilike(f"%{specialization}%")
        )

    doctors = query.all()

    result = []
    for d in doctors:
        result.append({
            "doctor_id": d.id,
            "user_id": d.user.id,
            "username": d.user.username,
            "email": d.user.email,
            "specialization": d.specialization,
            "experience_years": d.experience_years,
            "is_active": d.user.is_active
        })

    return result, 200

@admin_bp.route('/patients', methods=['GET'])
@jwt_required()
def get_patients():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return {"message": "Admin access required"}, 403

    username = request.args.get("username")

    query = Patient.query.join(User)

    if username:
        query = query.filter(
            User.username.ilike(f"%{username}%")
        )

    patients = query.all()

    result = []
    for p in patients:
        result.append({
            "patient_id": p.id,
            "user_id": p.user.id,
            "username": p.user.username,
            "email": p.user.email,
            "contact": getattr(p, "contact", None),
            "is_active": p.user.is_active
        })

    

    return result, 200

@admin_bp.route('/appointments', methods=['GET'])
@admin_required
def get_appointments():
    status = request.args.get("status")

    query = Appointment.query
    if status:
        query = query.filter(Appointment.status.ilike(f"%{status}%"))

    appointments = query.all()

    result = []
    for a in appointments:
        result.append({
            "appointment_id": a.id,
            "patient_username": a.patient.user.username,
            "doctor_username": a.doctor.user.username,
            "appointment_date": a.date.isoformat(),
            "status": a.status
        })

    return result, 200

@admin_bp.route('/user/<int:user_id>', methods=['PUT'])
@admin_required
def deactivate_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return {"message": "User not found"}, 404

    user.is_active = not user.is_active
    db.session.commit()

    return {
        "message": "User status updated successfully",
        "is_active": user.is_active
    }, 200

@admin_bp.route('/doctor/<int:doctor_id>', methods=['PUT'])
@admin_required
def update_doctor(doctor_id):
    data = request.get_json()

    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return {"message": "Doctor not found"}, 404

    if "specialization" in data:
        doctor.specialization = data["specialization"]

    if "experience_years" in data:
        doctor.experience_years = data["experience_years"]

    if "department_id" in data:
        doctor.department_id = data["department_id"]

    db.session.commit()
    return {"message": "Doctor updated successfully"}, 200

@admin_bp.route('/patient/<int:patient_id>', methods=['PUT'])
@admin_required
def update_patient(patient_id):
    data = request.get_json()

    patient = Patient.query.get(patient_id)
    if not patient:
        return {"message": "Patient not found"}, 404

    patient.contact = data.get("contact", patient.contact)
    patient.age = data.get("age", patient.age)
    patient.gender = data.get("gender", patient.gender)

    db.session.commit()

    return {
        "message": "Patient profile updated successfully",
        "patient_id": patient.id
    }, 200

@admin_bp.route('/run-daily-reminders', methods=['POST'])
@jwt_required()
def run_daily_reminders():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return {"message": "Admin access required"}, 403

    task = send_daily_reminders.delay()
    return {"message": "Daily reminders started", "task_id": task.id}, 202


