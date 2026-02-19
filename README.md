# 🏥 Hospital Management System (HMS)

> A full-stack web application for managing hospital operations — including patient appointments, doctor management, admin controls, automated reminders, and monthly reports — built with **Flask**, **Vue.js**, **Celery**, and **Redis**.

---

## 📌 Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Overview](#api-overview)
- [Background Tasks](#background-tasks)
- [Screenshots](#screenshots)
- [Author](#author)

---

## 🏨 About the Project

The **Hospital Management System (HMS)** is a comprehensive web application that streamlines core hospital workflows. It supports three types of users — **Admin**, **Doctor**, and **Patient** — each with their own dedicated dashboard and functionality.

Admins can manage doctors and view hospital-wide statistics. Doctors can manage their availability, view patient history, and handle appointments. Patients can book, cancel, or reschedule appointments and track their medical history.

The system also includes **automated background tasks** powered by Celery and Redis:
- 📬 **Daily reminders** are sent to patients with upcoming appointments.
- 📊 **Monthly reports** are auto-generated for admin review.
- 📁 **CSV exports** are available for appointment and patient data.

---

## ✨ Features

### 👤 Authentication
- Secure **JWT-based login & registration** for all user roles
- Role-based access control (Admin / Doctor / Patient)

### 🛡️ Admin Panel
- Add, Edit, and Remove Doctors
- View all patient records and appointments
- Access hospital-wide statistics and analytics
- Download CSV reports

### 🩺 Doctor Dashboard
- View assigned patient appointments
- Manage availability schedule
- Access complete patient history

### 🧑‍⚕️ Patient Dashboard
- Book appointments with available doctors
- View, cancel, or reschedule appointments
- View personal medical history and past visits
- Edit profile information

### ⏰ Automated Background Tasks
- **Daily Reminders** — Automatically sends appointment reminders every 2 minutes *(configurable)*
- **Monthly Reports** — Auto-generates hospital reports on the 1st of every month at 9:00 AM
- **CSV Export** — Export appointment/patient data as downloadable CSV files

### ⚡ Performance
- **Redis Caching** — Frequently accessed data is cached for fast responses
- **Celery Workers** — Heavy/async tasks run in background without blocking the main app

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **Python 3** | Core language |
| **Flask** | Web framework & REST API |
| **Flask-JWT-Extended** | JWT Authentication |
| **Flask-CORS** | Cross-Origin Resource Sharing |
| **SQLAlchemy** | ORM for database management |
| **SQLite** | Lightweight relational database |
| **Celery** | Asynchronous task queue |
| **Celery Beat** | Task scheduler (cron jobs) |
| **Redis** | Message broker + cache + result backend |

### Frontend
| Technology | Purpose |
|------------|---------|
| **Vue.js 3** | Frontend SPA framework |
| **Vue Router** | Client-side routing |
| **Vite** | Frontend build tool |
| **Axios** | HTTP client for API calls |
| **CSS3** | Custom styling |

---

## 📁 Project Structure

```
Hospital Management System/
│
├── backend/
│   ├── app.py                  # Main Flask application entry point
│   ├── celery_config.py        # Celery + Beat scheduler configuration
│   ├── auth_api.py             # Authentication endpoints (login/register)
│   ├── admin_api.py            # Admin-specific API routes
│   ├── doctor_api.py           # Doctor-specific API routes
│   ├── patient_api.py          # Patient-specific API routes
│   ├── cache.py                # Redis cache initialization
│   ├── seed_admin.py           # Script to seed default admin user
│   ├── reset_db.py             # Script to reset the database
│   ├── models/
│   │   └── models.py           # Database models (User, Doctor, Appointment, etc.)
│   ├── tasks/
│   │   ├── daily_reminder.py   # Celery task: daily appointment reminders
│   │   ├── monthly_report.py   # Celery task: monthly report generation
│   │   └── export_csv.py       # Celery task: CSV data export
│   ├── static/                 # Backend static files
│   └── instance/
│       └── hms_v2.db           # SQLite database file
│
├── frontend/
│   ├── src/
│   │   ├── views/
│   │   │   ├── Login.vue               # Login page
│   │   │   ├── Register.vue            # Patient registration
│   │   │   ├── AdminDashboard.vue      # Admin panel
│   │   │   ├── DoctorDashboard.vue     # Doctor panel
│   │   │   ├── PatientDashboard.vue    # Patient panel
│   │   │   ├── BookAppointment.vue     # Appointment booking
│   │   │   ├── PatientAppointments.vue # View appointments
│   │   │   ├── PatientReschedule.vue   # Reschedule appointments
│   │   │   ├── AppointmentCancel.vue   # Cancel appointment
│   │   │   ├── AppointmentComplete.vue # Mark appointment complete
│   │   │   ├── AddDoctor.vue           # Add new doctor (Admin)
│   │   │   ├── EditDoctor.vue          # Edit doctor details (Admin)
│   │   │   ├── PatientHistory.vue      # Patient medical history
│   │   │   ├── DoctorPatientHistory.vue# Doctor's view of patient history
│   │   │   ├── DoctorAvailability.vue  # Doctor availability management
│   │   │   └── EditProfile.vue         # Edit user profile
│   │   ├── router/
│   │   │   └── index.js                # Vue Router routes
│   │   ├── services/                   # API service layer (Axios)
│   │   └── assets/
│   │       └── style.css               # Global CSS styles
│   └── dist/                           # Production build output
│
├── run.sh                              # Shell script to run the full app
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

Make sure the following are installed on your system:
- Python 3.8+
- Node.js 16+ & npm
- Redis Server
- pip (Python package manager)

---

### 🔧 Backend Setup

```bash
# 1. Go to the backend folder
cd backend

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Seed the default admin user
python seed_admin.py

# 5. Start the Flask server
python app.py
```

> Flask will run at: **http://127.0.0.1:5000**

---

### 🎨 Frontend Setup

```bash
# 1. Go to the frontend folder
cd frontend

# 2. Install Node dependencies
npm install

# 3. Build the frontend for production
npm run build

# OR run in development mode
npm run dev
```

---

### ⚙️ Start Celery Worker & Beat Scheduler

Open **two separate terminals** in the `backend/` folder:

```bash
# Terminal 1 — Start Celery Worker
celery -A celery_config.celery worker --loglevel=info --pool=solo

# Terminal 2 — Start Celery Beat (Scheduler)
celery -A celery_config.celery beat --loglevel=info
```

> ⚠️ **Redis must be running** before starting Celery.  
> Start Redis: `redis-server`

---

### 🔑 Default Admin Credentials

After running `seed_admin.py`, use:

```
Email:    admin@hms.com
Password: admin123
```

---

## 🔗 API Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/login` | Login (all roles) |
| `POST` | `/api/auth/register` | Register new patient |
| `GET` | `/api/admin/doctors` | List all doctors |
| `POST` | `/api/admin/add-doctor` | Add a new doctor |
| `PUT` | `/api/admin/edit-doctor/<id>` | Edit doctor details |
| `DELETE` | `/api/admin/delete-doctor/<id>` | Delete a doctor |
| `GET` | `/api/doctor/appointments` | Doctor's appointments |
| `GET` | `/api/doctor/patient-history` | View patient history |
| `GET` | `/api/patient/appointments` | Patient's appointments |
| `POST` | `/api/patient/book` | Book an appointment |
| `PUT` | `/api/patient/reschedule/<id>` | Reschedule appointment |
| `DELETE` | `/api/patient/cancel/<id>` | Cancel an appointment |
| `GET` | `/api/admin/export-csv` | Export data as CSV |

---

## ⏱️ Background Tasks (Celery Beat Schedule)

| Job Name | Task | Schedule |
|----------|------|----------|
| `daily-reminder-job` | Send appointment reminders to patients | Every 2 minutes *(demo)* |
| `monthly-report-job` | Generate and send monthly hospital report | 1st of every month, 9:00 AM IST |
| `export-csv-job` | Export patient/appointment data to CSV | On-demand (triggered via API) |

---

## 👨‍💻 Author

**Anjali Kokare**  
📧 anjalikokare658@gmail.com  
🎓 B.Sc. in Data Science and Applications — IIT Madras  

---

## 📄 License

This project is developed for educational purposes as part of an academic project.

---

> ⭐ If you found this project helpful, feel free to star the repository!
