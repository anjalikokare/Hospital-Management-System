import os
import smtplib
import csv
import io
from datetime import date, timedelta
from collections import Counter
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from celery_config import celery
from models.models import Doctor, Appointment, Treatment
SMTP_SERVER = "localhost"
SMTP_PORT = 1025
SENDER_EMAIL = "anjalirkokare@gmail.com"
def send_report_email(doctor_name, doctor_email, month_tag, appts, diag_counts):
    try:
        email_body = f"""
Dear Dr. {doctor_name},

This is your monthly activity report for {month_tag}.

Summary:
- Total Appointments: {len(appts)}
- Top Diagnoses:
"""
        for diag, count in diag_counts.most_common(5):
            email_body += f"  * {diag.title()}: {count} cases\n"
        email_body += "\nDetailed appointment list is attached as a CSV file for your records.\n\nBest regards,\nHMS Team"
        msg = MIMEMultipart()
        msg['Subject'] = f'Monthly Report - {doctor_name} - {month_tag}'
        msg['From'] = SENDER_EMAIL
        msg['To'] = doctor_email
        msg.attach(MIMEText(email_body, "plain"))
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Date", "Time", "Patient", "Diagnosis", "Prescription"])
        for a in appts:
            t = Treatment.query.filter_by(appointment_id=a.id).first()
            writer.writerow([a.date, a.time, a.patient.user.username, (t.diagnosis if t else ""), (t.prescription if t else "")])
        part = MIMEBase("application", "octet-stream")
        part.set_payload(output.getvalue())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename=report_{month_tag.replace(' ', '_')}.csv")
        msg.attach(part)
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.send_message(msg)
        server.quit()
    except Exception:
        pass
@celery.task(name="tasks.monthly_report.generate_monthly_reports")
def generate_monthly_reports():
    today = date.today()
    start = today.replace(day=1)
    end = today + timedelta(days=1)
    month_tag = start.strftime("%B %Y")
    doctors = Doctor.query.all()
    for d in doctors:
        appts = (Appointment.query
                .filter(Appointment.doctor_id == d.id, Appointment.date >= start, Appointment.date < end)
                .order_by(Appointment.date.asc()).all())
        diagnoses = []
        for a in appts:
            t = Treatment.query.filter_by(appointment_id=a.id).first()
            if t and t.diagnosis:
                diagnoses.append(t.diagnosis.strip().lower())
        diag_counts = Counter(diagnoses)
        send_report_email(d.user.username, d.user.email, month_tag, appts, diag_counts)
    return {"month": month_tag, "doctors": len(doctors)}
@celery.task(name="tasks.monthly_report.send_treatment_email")
def send_treatment_email(appointment_id):
    try:
        appt = Appointment.query.get(appointment_id)
        if not appt or not appt.treatment:
            return "Error"
        patient_name = appt.patient.user.username
        patient_email = appt.patient.user.email
        doctor_name = appt.doctor.user.username
        date_str = appt.date.strftime("%B %d, %Y")
        t = appt.treatment
        body = f"""Hi {patient_name},
This is your medical report for your visit with Dr. {doctor_name} on {date_str}.
Diagnosis: {t.diagnosis or 'N/A'}
Prescription: {t.prescription or 'N/A'}
Doctor's Notes: {t.notes or 'N/A'}
Best regards,
HMS Team
"""
        msg = MIMEText(body)
        msg['Subject'] = f'Medical Report - Visit on {date_str}'
        msg['From'] = SENDER_EMAIL
        msg['To'] = patient_email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.send_message(msg)
        server.quit()
        return "Sent"
    except Exception:
        return "Failed"
