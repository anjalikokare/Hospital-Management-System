import csv
import os
from celery_config import celery
from flask import current_app
from models.models import Treatment, Appointment

@celery.task(name="tasks.export_csv.export_treatment_history")
def export_treatment_history(patient_id):
    try:
        static_dir = os.path.join(current_app.static_folder, "exports")
        os.makedirs(static_dir, exist_ok=True)

        filename = f"treatment_history_{patient_id}.csv"
        file_path = os.path.join(static_dir, filename)

        treatments = (
            Treatment.query
            .join(Appointment)
            .filter(Appointment.patient_id == patient_id)
            .order_by(Appointment.date.asc())
            .all()
        )

        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
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

        print(f"✅ CSV Export ready: {file_path}")
        return f"static/exports/{filename}"

    except Exception as e:
        print("❌ Export failed:", str(e))
        raise e
