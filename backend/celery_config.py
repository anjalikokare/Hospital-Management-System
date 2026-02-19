from celery import Celery
from flask import Flask
from models.models import db
from celery.schedules import crontab


def create_flask_app():
    app = Flask("celery_worker")

    app.config.update(
        SQLALCHEMY_DATABASE_URI="sqlite:///hms_v2.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        broker_url="redis://127.0.0.1:6379/0",
        result_backend="redis://127.0.0.1:6379/0",
    )

    db.init_app(app)
    return app


flask_app = create_flask_app()

celery = Celery(
    flask_app.import_name,
    broker=flask_app.config["broker_url"],
    backend=flask_app.config["result_backend"],
)

celery.conf.update(
    timezone="Asia/Kolkata",
    enable_utc=True,
)


class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with flask_app.app_context():
            return self.run(*args, **kwargs)


celery.Task = ContextTask

celery.conf.beat_schedule = {
    "daily-reminder-job": {
        "task": "tasks.daily_reminder.send_daily_reminders",
        "schedule": crontab(minute="*/2"),
    },
    "monthly-report-job": {
        "task": "tasks.monthly_report.generate_monthly_reports",
        "schedule": crontab(day_of_month=1, hour=9, minute=0),
    },
}


import tasks.export_csv
import tasks.daily_reminder
import tasks.monthly_report
