from datetime import date
from celery_config import celery
from models.models import Appointment

@celery.task(name="tasks.daily_reminder.send_daily_reminders")
def send_daily_reminders():
    today = date.today()

    appts = (Appointment.query
             .filter(Appointment.date == today, Appointment.status == "Booked")
             .all())

    for a in appts:
        patient_email = a.patient.user.email
        patient_name = a.patient.user.username
        doctor_name = a.doctor.user.username
        print(f"📩 Reminder -> {patient_email} | Hi {patient_name}, today appointment with Dr. {doctor_name} at {a.time}")

    print(f"✅ Daily reminders sent: {len(appts)}")
    return len(appts)
