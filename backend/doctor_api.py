from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from datetime import date, timedelta, datetime
import os
from models.models import Doctor, Patient, User, Appointment, Treatment, Availability, db
from tasks.monthly_report import generate_monthly_reports, send_treatment_email
from cache import cache


doctor_bp = Blueprint('doctor', __name__)


@doctor_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    claims = get_jwt()
    user_id = int(get_jwt_identity())
    if claims.get("role") != "doctor":
        return {"message": "Doctor access required"}, 403
    doctor = Doctor.query.filter_by(user_id=user_id).first()
    if not doctor:
        return {"message": "Doctor profile not found"}, 404
    today = date.today()
    next_week = today + timedelta(days=7)
    appointments = Appointment.query.filter_by(
        doctor_id=doctor.id
    ).all()
    today_count = 0
    upcoming_count = 0
    patient_ids = set()
    for a in appointments:
        if a.status != "Cancelled":
            patient_ids.add(a.patient_id)
        if a.status != "Booked":
            continue
        if a.date == today:
            today_count += 1
        if today < a.date <= next_week:
            upcoming_count += 1
    return {
        "today": today_count,
        "upcoming": upcoming_count,
        "patients": len(patient_ids)
    }, 200


@doctor_bp.route('/appointments', methods=['GET'])
@jwt_required()
def get_appointments():
    claims = get_jwt()
    user_id = int(get_jwt_identity())
    if claims.get("role") != "doctor":
        return {"message": "Doctor access required"}, 403
    doctor = Doctor.query.filter_by(user_id=user_id).first()
    if not doctor:
        return {"message": "Doctor profile not found"}, 404
    appointments = Appointment.query.filter_by(
        doctor_id=doctor.id
    ).all()
    result = []
    for a in appointments:
        result.append({
            "appointment_id": a.id,
            "patient": a.patient.user.username,
            "date": a.date.isoformat(),
            "time": a.time,
            "status": a.status
        })
    return result, 200


@doctor_bp.route('/patients', methods=['GET'])
@jwt_required()
def get_patients():
    claims = get_jwt()
    user_id = int(get_jwt_identity())
    if claims.get("role") != "doctor":
        return {"message": "Doctor access required"}, 403
    doctor = Doctor.query.filter_by(user_id=user_id).first()
    if not doctor:
        return {"message": "Doctor profile not found"}, 404
    appointments = Appointment.query.filter_by(
        doctor_id=doctor.id
    ).all()
    seen = set()
    patients = []
    for a in appointments:
        if a.patient.id not in seen:
            seen.add(a.patient.id)
            patients.append({
                "name": a.patient.user.username,
                "last_visit": a.date.isoformat()
            })
    return patients, 200


@doctor_bp.route('/appointment/<int:appointment_id>/status', methods=['PUT'])
@jwt_required()
def update_appointment_status(appointment_id):
    claims = get_jwt()
    user_id = int(get_jwt_identity())
    if claims.get("role") != "doctor":
        return {"message": "Doctor access required"}, 403
    doctor = Doctor.query.filter_by(user_id=user_id).first()
    appointment = Appointment.query.get(appointment_id)
    if not appointment or appointment.doctor_id != doctor.id:
        return {"message": "Appointment not found"}, 404
    data = request.get_json()
    status = data.get("status")
    if status not in ["Completed", "Cancelled"]:
        return {"message": "Invalid status"}, 400
    appointment.status = status
    db.session.commit()
    return {"message": "Appointment updated"}, 200


@doctor_bp.route('/appointment/<int:appointment_id>/treatment', methods=['POST'])
@jwt_required()
def add_treatment(appointment_id):
    claims = get_jwt()
    user_id = int(get_jwt_identity())
    if claims.get("role") != "doctor":
        return {"message": "Doctor access required"}, 403
    doctor = Doctor.query.filter_by(user_id=user_id).first()
    appointment = Appointment.query.get(appointment_id)
    if not appointment or appointment.doctor_id != doctor.id:
        return {"message": "Appointment not found"}, 404
    existing = Treatment.query.filter_by(
        appointment_id=appointment.id
    ).first()
    if existing:
        return {
            "message": "Treatment already added"
        }, 409
    data = request.get_json()
    treatment = Treatment(
        appointment_id=appointment.id,
        diagnosis=data.get("diagnosis"),
        prescription=data.get("prescription"),
        notes=data.get("notes")
    )
    appointment.status = "Completed"
    db.session.add(treatment)
    db.session.commit()
    send_treatment_email.delay(appointment.id)
    return {"message": "Appointment completed"}, 201


@doctor_bp.route('/patient/<string:username>/history', methods=['GET'])
@jwt_required()
def get_patient_history(username):
    claims = get_jwt()
    if claims.get("role") != "doctor":
        return {"message": "Doctor access required"}, 403
    treatments = (
        Treatment.query
        .join(Appointment)
        .join(Patient)
        .join(User)
        .filter(User.username == username)
        .all()
    )
    result = []
    for t in treatments:
        result.append({
            "date": t.appointment.date.isoformat(),
            "diagnosis": t.diagnosis,
            "prescription": t.prescription,
            "notes": t.notes
        })
    return result, 200


@doctor_bp.route('/availability', methods=['POST'])
@jwt_required()
def update_availability():
    claims = get_jwt()
    user_id = int(get_jwt_identity())
    if claims.get("role") != "doctor":
        return {"message": "Doctor access required"}, 403
    doctor = Doctor.query.filter_by(user_id=user_id).first()
    if not doctor:
        return {"message": "Doctor profile not found"}, 404
    data = request.get_json()
    date_str = data.get("date")
    morning = data.get("morning_slot", False)
    evening = data.get("evening_slot", False)
    if not date_str:
        return {"message": "Date required"}, 400
    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    availability = Availability.query.filter_by(
        doctor_id=doctor.id,
        date=date_obj
    ).first()
    if availability:
        availability.morning_slot = morning
        availability.evening_slot = evening
    else:
        availability = Availability(
            doctor_id=doctor.id,
            date=date_obj,
            morning_slot=morning,
            evening_slot=evening
        )
        db.session.add(availability)
    db.session.commit()
    cache.delete(f"doctor_availability:{doctor.id}")
    cache.delete(f"doctor_availability:{doctor.id}:{date_obj.isoformat()}")
    return {"message": "Availability updated successfully"}, 200

    
@doctor_bp.route('/monthly-report/generate', methods=['POST'])
@jwt_required()
def generate_monthly_report():
    claims = get_jwt()
    if claims.get("role") != "doctor":
        return {"message": "Doctor access required"}, 403
    user_id = int(get_jwt_identity())
    doctor = Doctor.query.filter_by(user_id=user_id).first()
    if not doctor:
        return {"message": "Doctor profile not found"}, 404
    generate_monthly_reports.delay()
    return {"message": "Report sent to your email successfully"}, 200


