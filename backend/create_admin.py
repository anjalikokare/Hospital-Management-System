from app import app
from models.models import db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    admin = User.query.filter_by(role="admin").first()

    if not admin:
        admin = User(
            username="admin",
            email="admin@hms.com",
            password=generate_password_hash("admin123"),
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created")
    else:
        print("Admin already exists")


