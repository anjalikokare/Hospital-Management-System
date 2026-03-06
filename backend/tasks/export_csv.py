import csv
import os
import smtplib
import io
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from celery_config import celery
from flask import current_app
from models.models import Treatment, Appointment, Doctor, Patient, User

SMTP_SERVER = "localhost"
SMTP_PORT = 1025
SENDER_EMAIL = "anjalirkokare@gmail.com"
@celery.task(name="tasks.export_csv.export_treatment_history")
def export_treatment_history(patient_id):
    try:
        patient = Patient.query.get(patient_id)
        if not patient:
            return "Patient not found"
        treatments = (
            Treatment.query
            .join(Appointment)
            .filter(Appointment.patient_id == patient_id)
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
        body = f"""Hi {patient.user.username},
This is your requested medical treatment history export.
Best regards,
HMS Team"""
        msg = MIMEMultipart()
        msg['Subject'] = 'Your Medical Records Export'
        msg['From'] = SENDER_EMAIL
        msg['To'] = patient.user.email
        msg.attach(MIMEText(body, "plain"))
        part = MIMEBase("application", "octet-stream")
        part.set_payload(output.getvalue())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment; filename=medical_history.csv")
        msg.attach(part)
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.send_message(msg)
        server.quit()
        return "Email sent successfully"
    except Exception as e:
        raise e
@celery.task(name="tasks.export_csv.export_all_data")
def export_all_data():
    try:
        static_dir = os.path.join(current_app.static_folder, "exports")
        os.makedirs(static_dir, exist_ok=True)
        filename = "full_hospital_data.csv"
        file_path = os.path.join(static_dir, filename)
        appointments = Appointment.query.all()
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Patient", "Doctor", "Date", "Status"])
            for a in appointments:
                writer.writerow([
                    a.id,
                    a.patient.user.username,
                    a.doctor.user.username,
                    a.date.isoformat(),
                    a.status
                ])
        return f"static/exports/{filename}"
    except Exception as e:
        raise e


