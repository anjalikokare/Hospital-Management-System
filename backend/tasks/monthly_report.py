import os
from datetime import date, timedelta
from collections import Counter
from celery_config import celery
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from models.models import Doctor, Appointment, Treatment

@celery.task(name="tasks.monthly_report.generate_monthly_reports")
def generate_monthly_reports():
    today = date.today()
    first_day_this_month = today.replace(day=1)
    last_day_prev_month = first_day_this_month - timedelta(days=1)
    first_day_prev_month = last_day_prev_month.replace(day=1)

    start = first_day_this_month
    end = today + timedelta(days=1)   


    base_dir = os.path.dirname(os.path.abspath(__file__))    
    reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static", "reports"))
    os.makedirs(reports_dir, exist_ok=True)


    month_tag = start.strftime("%B_%Y")

    doctors = Doctor.query.all()
    for d in doctors:
        appts = (
            Appointment.query
            .filter(
                Appointment.doctor_id == d.id,
                Appointment.date >= start,
                Appointment.date < end,
            )
            .order_by(Appointment.date.asc())
            .all()
        )
        diagnoses = []
        for a in appts:
            t = Treatment.query.filter_by(appointment_id=a.id).first()
            if t and t.diagnosis:
                diag = t.diagnosis.strip().lower().rstrip(".")
                diagnoses.append(diag)

        diag_counts = Counter(diagnoses)

        filename = f"doctor_{d.id}_report_{month_tag}.pdf"
        file_path = os.path.join(reports_dir, filename)

        c = canvas.Canvas(file_path, pagesize=letter)
        y = 750
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, f"Monthly Doctor Report: {month_tag}")
        y -= 20
        c.setFont("Helvetica", 12)
        c.drawString(50, y, f"Doctor: Dr. {d.user.username} | Specialization: {d.specialization}")
        y -= 20
        c.drawString(50, y, f"Period: {start.isoformat()} to {(end - timedelta(days=1)).isoformat()}")
        y -= 30

        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"Total Appointments: {len(appts)}")
        y -= 20

        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Appointments:")
        y -= 18
        c.setFont("Helvetica", 10)

        if not appts:
            c.drawString(50, y, "No appointments in this month.")
            y -= 14
        else:
            for a in appts:
                patient_name = a.patient.user.username
                t = Treatment.query.filter_by(appointment_id=a.id).first()
                dx = (t.diagnosis[:60] if (t and t.diagnosis) else "")
                line = f"{a.date.isoformat()} {a.time} | Patient: {patient_name} | Status: {a.status} | Dx: {dx}"
                c.drawString(50, y, line)
                y -= 14
                if y < 80:
                    c.showPage()
                    y = 750
                    c.setFont("Helvetica", 10)

        y -= 10
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Diagnosis Summary (Top 10):")
        y -= 18
        c.setFont("Helvetica", 10)

        if not diag_counts:
            c.drawString(50, y, "No diagnosis records found.")
            y -= 14
        else:
            for diag, cnt in diag_counts.most_common(10):
                c.drawString(50, y, f"{diag}  ->  {cnt}")
                y -= 14
                if y < 80:
                    c.showPage()
                    y = 750
                    c.setFont("Helvetica", 10)

        c.save()
        print(f"✅ Monthly report generated: {file_path}")

    return {"month": month_tag, "doctors": len(doctors)}
