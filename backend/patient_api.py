from flask import Blueprint, request, jsonify, Response
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime
from models.models import Doctor, Patient, Appointment, Availability, Treatment, User, db
from celery_config import celery
from cache import cache
import io
import csv
from flask import send_from_directory

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/doctors', methods=['GET'])
@jwt_required()
@cache.cached(timeout=300, query_string=True)
def get_doctors():
    claims = get_jwt()
    if claims.get("role") != "patient":
        return {"message": "Only patients can view doctors"}, 403
    search = request.args.get("search")
    query = Doctor.query.join(User)
    if search:
        query = query.filter(
            (User.username.ilike(f"%{search}%")) |
            (Doctor.specialization.ilike(f"%{search}%"))
        )
    doctors = query.all()
    result = []
    for d in doctors:
        result.append({
            "doctor_id": d.id,
            "username": d.user.username,
            "email": d.user.email,
            "specialization": d.specialization,
            "experience_years": d.experience_years
        })
    return result, 200

@patient_bp.route('/doctor/<int:doctor_id>/availability', methods=['GET'])
@jwt_required()
def get_doctor_availability(doctor_id):
    claims = get_jwt()
    if claims.get("role") != "patient":
        return {"message": "Patient access required"}, 403
    cache_key = f"doctor_availability:{doctor_id}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached, 200
    availability = Availability.query.filter_by(doctor_id=doctor_id).all()
    result = []
    for a in availability:
        result.append({
            "date": a.date.isoformat(),
            "morning_slot": a.morning_slot,
            "evening_slot": a.evening_slot
        })
    cache.set(cache_key, result, timeout=120)
    return result, 200

@patient_bp.route('/appointment', methods=['POST'])
@jwt_required()
def create_appointment():
    user_id = int(get_jwt_identity())
    claims = get_jwt()
    if claims.get("role") != "patient":
        return {"message": "Only patients can book appointments"}, 403
    data = request.get_json()
    doctor_id = data.get("doctor_id")
    date = data.get("date")
    time = data.get("time")
    if not doctor_id or not date or not time:
        return {"message": "Missing required fields"}, 400
    patient = Patient.query.filter_by(user_id=user_id).first()
    if not patient:
        return {"message": "Patient profile not found"}, 404
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return {"message": "Doctor not found"}, 404
    appointment_date = datetime.strptime(date, "%Y-%m-%d").date()
    availability = Availability.query.filter_by(
        doctor_id=doctor.id,
        date=appointment_date
    ).first()
    if not availability:
        return {"message": "Doctor not available on this date"}, 400
    if time < "12:00" and not availability.morning_slot:
        return {"message": "Doctor not available in morning slot"}, 400
    if time >= "12:00" and not availability.evening_slot:
        return {"message": "Doctor not available in evening slot"}, 400
    conflict = Appointment.query.filter(
        Appointment.doctor_id == doctor.id,
        Appointment.date == appointment_date,
        Appointment.time == time,
        Appointment.status != "Cancelled"
    ).first()
    if conflict:
        return {"message": "Slot already booked"}, 409
    appointment = Appointment(
        doctor_id=doctor.id,
        patient_id=patient.id,
        date=appointment_date,
        time=time,
        status="Booked"
    )
    db.session.add(appointment)
    db.session.commit()
    return {"message": "Appointment booked successfully"}, 201

@patient_bp.route('/appointments', methods=['GET'])
@jwt_required()
def get_appointments():
    claims = get_jwt()
    user_id = int(get_jwt_identity())
    if claims.get("role") != "patient":
        return {"message": "Patient access required"}, 403
    patient = Patient.query.filter_by(user_id=user_id).first()
    if not patient:
        return {"message": "Patient profile not found"}, 404
    appointments = Appointment.query.filter_by(
        patient_id=patient.id
    ).all()
    result = []
    for a in appointments:
        result.append({
            "appointment_id": a.id,
            "doctor_username": a.doctor.user.username,
            "date": a.date.isoformat(),
            "time": a.time,
            "status": a.status
        })
    return result, 200

@patient_bp.route('/appointment/<int:appointment_id>/reschedule', methods=['PUT'])
@jwt_required()
def reschedule_appointment(appointment_id):
    user_id = int(get_jwt_identity())
    claims = get_jwt()
    if claims.get("role") != "patient":
        return {"message": "Only patients can reschedule"}, 403
    data = request.get_json()
    new_date = data.get("date")
    new_time = data.get("time")
    if not new_date or not new_time:
        return {"message": "Date and time required"}, 400
    patient = Patient.query.filter_by(user_id=user_id).first()
    appointment = Appointment.query.get(appointment_id)
    if not appointment or appointment.patient_id != patient.id:
        return {"message": "Appointment not found"}, 404
    if appointment.status != "Booked":
        return {"message": "Only booked appointments can be rescheduled"}, 400
    appointment_date = datetime.strptime(new_date, "%Y-%m-%d").date()
    availability = Availability.query.filter_by(
        doctor_id=appointment.doctor_id,
        date=appointment_date
    ).first()
    if not availability:
        return {"message": "Doctor not available on this date"}, 400
    if new_time < "12:00" and not availability.morning_slot:
        return {"message": "Doctor not available in morning slot"}, 400
    if new_time >= "12:00" and not availability.evening_slot:
        return {"message": "Doctor not available in evening slot"}, 400
    conflict = Appointment.query.filter(
        Appointment.doctor_id == appointment.doctor_id,
        Appointment.date == appointment_date,
        Appointment.time == new_time,
        Appointment.status != "Cancelled",
        Appointment.id != appointment.id
    ).first()
    if conflict:
        return {"message": "Slot already booked"}, 409
    appointment.date = appointment_date
    appointment.time = new_time
    db.session.commit()
    return {"message": "Appointment rescheduled successfully"}, 200

@patient_bp.route('/appointment/<int:appointment_id>/cancel', methods=['PUT'])
@jwt_required()
def cancel_appointment(appointment_id):
    user_id = int(get_jwt_identity())
    claims = get_jwt()
    if claims.get("role") != "patient":
        return {"message": "Only patients can cancel"}, 403
    patient = Patient.query.filter_by(user_id=user_id).first()
    appointment = Appointment.query.get(appointment_id)
    if not appointment or appointment.patient_id != patient.id:
        return {"message": "Appointment not found"}, 404
    if appointment.status != "Booked":
        return {"message": "Only booked appointments can be cancelled"}, 400
    appointment.status = "Cancelled"
    db.session.commit()
    return {"message": "Appointment cancelled successfully"}, 200

@patient_bp.route('/medical-history', methods=['GET'])
@jwt_required()
def get_medical_history():
    claims = get_jwt()
    user_id = int(get_jwt_identity())
    if claims.get("role") != "patient":
        return {"message": "Patient access required"}, 403
    patient = Patient.query.filter_by(user_id=user_id).first()
    if not patient:
        return {"message": "Patient profile not found"}, 404
    treatments = (
        Treatment.query
        .join(Appointment)
        .filter(Appointment.patient_id == patient.id)
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

@patient_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = int(get_jwt_identity())
    claims = get_jwt()
    if claims.get("role") != "patient":
        return {"message": "Patient access required"}, 403
    patient = Patient.query.filter_by(user_id=user_id).first()
    if not patient:
        return {"message": "Patient profile not found"}, 404
    return {
        "contact": patient.contact or "",
        "age": patient.age or "",
        "gender": patient.gender or "",
        "address": patient.address or ""
    }, 200

@patient_bp.route('/profile', methods=['PUT'])
@jwt_required()
def edit_profile():
    user_id = int(get_jwt_identity())
    claims = get_jwt()
    if claims.get("role") != "patient":
        return {"message": "Patient access required"}, 403
    data = request.get_json()
    patient = Patient.query.filter_by(user_id=user_id).first()
    if not patient:
        return {"message": "Patient profile not found"}, 404
    patient.contact = data.get("contact", patient.contact)
    patient.age = data.get("age", patient.age)
    patient.gender = data.get("gender", patient.gender)
    patient.address = data.get("address", patient.address)
    db.session.commit()
    return {"message": "Profile updated successfully"}, 200

@patient_bp.route('/appointment/<int:appointment_id>/availability', methods=['GET'])
@jwt_required()
def get_reschedule_availability(appointment_id):
    claims = get_jwt()
    if claims.get("role") != "patient":
        return {"message": "Patient access required"}, 403
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return {"message": "Appointment not found"}, 404
    availability = Availability.query.filter_by(
        doctor_id=appointment.doctor_id
    ).all()
    result = []
    for a in availability:
        result.append({
            "date": a.date.isoformat(),
            "morning_slot": a.morning_slot,
            "evening_slot": a.evening_slot
        })
    return result, 200

@patient_bp.route('/export', methods=['GET'])
@jwt_required()
def export_history():
    user_id = int(get_jwt_identity())
    patient = Patient.query.filter_by(user_id=user_id).first()
    if not patient:
        return {"message": "Patient not found"}, 404
    treatments = (
        Treatment.query
        .join(Appointment)
        .filter(Appointment.patient_id == patient.id)
        .order_by(Appointment.date.asc())
        .all()
    )
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Date", "Doctor", "Diagnosis", "Prescription", "Notes"])
    for t in treatments:
        a = t.appointment
        writer.writerow([
            a.date.isoformat(),
            a.doctor.user.username,
            t.diagnosis or "",
            t.prescription or "",
            t.notes or "",
        ])
    response = Response(output.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=medical_history.csv"
    return response

@patient_bp.route("/static/exports/<filename>")
def download_export(filename):
    return send_from_directory("static/exports", filename)
