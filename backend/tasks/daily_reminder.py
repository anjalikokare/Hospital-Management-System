import smtplib
from email.mime.text import MIMEText
from datetime import date
from celery_config import celery
from models.models import Appointment
@celery.task(name="tasks.daily_reminder.send_daily_reminders")
def send_daily_reminders():
    today = date.today()
    try:
        appts = (Appointment.query
                 .filter(Appointment.date == today, Appointment.status == "Booked")
                 .all())
        if not appts:
            return 0
        smtp_server = "localhost"
        smtp_port = 1025
        sender_email = "anjalirkokare@gmail.com"
        server = smtplib.SMTP(smtp_server, smtp_port)
        sent_count = 0
        for a in appts:
            patient_name = a.patient.user.username
            patient_email = a.patient.user.email
            doctor_name = a.doctor.user.username
            target_email = sender_email 
            body = f"Hi {patient_name}\n\nThis is a reminder for your appointment with Dr. {doctor_name} today at {a.time}.\n\nBest regards,\nHMS Team"
            msg = MIMEText(body)
            msg['Subject'] = f'Appointment Reminder - {patient_name}'
            msg['From'] = sender_email
            msg['To'] = target_email
            server.send_message(msg)
            sent_count += 1
        server.quit()
        return sent_count
    except Exception:
        return 0
