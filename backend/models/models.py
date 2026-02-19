from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"


class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)

    doctors = db.relationship("Doctor", backref="department", lazy=True)

    def __repr__(self):
        return f"<Department {self.name}>"


class Doctor(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    experience_years = db.Column(db.Integer)

    user = db.relationship("User", backref=db.backref("doctor", uselist=False))
    appointments = db.relationship("Appointment", backref="doctor", lazy=True)
    availability = db.relationship("Availability", backref="doctor", lazy=True)

    def __repr__(self):
        return f"<Doctor user_id={self.user_id}>"


class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    contact = db.Column(db.String(20))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    address = db.Column(db.Text)

    user = db.relationship("User", backref=db.backref("patient", uselist=False))
    appointments = db.relationship("Appointment", backref="patient", lazy=True)

    def __repr__(self):
        return f"<Patient user_id={self.user_id}>"


class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.String(20))
    status = db.Column(db.String(20), default="Booked")

    def __repr__(self):
        return f"<Appointment {self.id} - {self.status}>"


class Availability(db.Model):
    __tablename__ = "availability"

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    morning_slot = db.Column(db.Boolean, default=False)
    evening_slot = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Availability doctor_id={self.doctor_id} date={self.date}>"


class Treatment(db.Model):
    __tablename__ = "treatments"

    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointments.id"), nullable=False, unique=True)
    diagnosis = db.Column(db.Text)
    prescription = db.Column(db.Text)
    notes = db.Column(db.Text)

    appointment = db.relationship("Appointment", backref=db.backref("treatment", uselist=False))

    def __repr__(self):
        return f"<Treatment appointment_id={self.appointment_id}>"
