import smtplib
from email.mime.text import MIMEText
from datetime import date
from celery_config import celery
from models.models import Appointment

@celery.task(name="tasks.daily_reminder.send_daily_reminders")
def send_daily_reminders():
    today = date.today()
    print(f"Running daily reminders for date: {today}")

    try:
        appts = (Appointment.query
                 .filter(Appointment.date == today, Appointment.status == "Booked")
                 .all())

        if not appts:
            print("No booked appointments for today.")
            return 0

        # SMTP Configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "anjalirkokare@gmail.com"
        sender_password = "wzti tkof zqoq rifb"

        # Create SMTP connection
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        sent_count = 0
        for a in appts:
            patient_name = a.patient.user.username
            patient_email = a.patient.user.email
            doctor_name = a.doctor.user.username
            
            # IMPORTANT: For testing/viva, we send all emails to the Admin's email
            # In a real app, this would be 'patient_email'
            target_email = sender_email 
            
            body = f"Hi {patient_name} (Test Mode),\n\nThis is a reminder for your appointment with Dr. {doctor_name} today at {a.time}.\n\nBest regards,\nHMS Team"
            msg = MIMEText(body)
            msg['Subject'] = f'Appointment Reminder - {patient_name}'
            msg['From'] = sender_email
            msg['To'] = target_email

            server.send_message(msg)
            print(f"✅ Reminder sent to {patient_name} ({target_email})")
            sent_count += 1

        server.quit()
        print(f"🏁 Finished task. Total reminders sent: {sent_count}")
        return sent_count

    except Exception as e:
        print(f"❌ Error in send_daily_reminders: {str(e)}")
        return 0
