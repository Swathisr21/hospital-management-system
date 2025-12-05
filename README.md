PES Hospital Management System

A full-stack web-based Hospital Management System designed to streamline patient care, improve hospital administration, and automate routine medical processes.
This system provides dedicated dashboards for Admin, Doctor, and Patient with secure role-based authentication.

==> Features
1, Doctor Module

View daily appointments

Accept / reject appointment requests

Manage time slots & availability

Write and upload prescriptions

View patient history and reports

Dashboard showing patient count

2, Patient Module

Register & secure login

Book appointments

Download prescriptions

View consultation history

Upload medical reports

Track appointment status

3, Admin Module

Add / manage doctors

Manage doctor availability

View all appointments

Monitor hospital activity

Dashboard analytics

Department & doctor-wise stats

4, Authentication & Roles

Password hashing (Werkzeug)

Role-based access:

Admin

Doctor

Patient

Protected routes (Flask-Login)

5, Appointment Approval Logic

Patient books an appointment

Request goes to the doctor

Doctor approves or rejects

Patient sees status update

==> Analytics update automatically

==> Folder Structure
hospital-management-system/
│
├── static/
│   ├── css/
│   ├── images/
│   └── reports/
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── patient.html
│   ├── doctor_list.html
│   ├── doctor_schedule.html
│   ├── prescribe.html
│   ├── upload_report.html
│   ├── view_prescriptions.html
│   ├── bill.html
│   ├── admin.html
│   └── history.html
│
├── main.py
├── models.py
├── features.py
├── requirements.txt
├── hospital.sql
└── README.md

==> Tech Stack
Frontend:

HTML5

CSS3

Bootstrap 5

Tailwind CSS (optional)

JavaScript

Backend:

Python Flask

Flask-SQLAlchemy

Flask-Login

Database:

MySQL

SQLAlchemy ORM

--> Installation
1. Clone the Repository
git clone https://github.com/Swathisr21/hospital-management-system.git
cd hospital-management-system

2.Create Virtual Environment
python -m venv venv
venv\Scripts\activate

3. Install Requirements
pip install -r requirements.txt

4.Import Database

Import hospital.sql into MySQL.

5. Configure Database Connection

Inside main.py:

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:yourpassword@localhost/hospital"

6. Run the App
python main.py


Access the project at:
--> http://127.0.0.1:5000/

--> ER Diagram

Patients (1) —— (M) Appointments (M) —— (1) Doctors
                │                       │
                │—— (1) Billing         │
                │—— (M) Reports         │
                └—— (M) Prescriptions ——
    <img width="1536" height="1024" alt="ERD" src="https://github.com/user-attachments/assets/35ad1b4b-d6cd-4ef9-90d3-772e3007b2c5" />

           

--> UML Diagrams
Use Case Diagram

Admin manages doctors

Patient books appointments

Doctor approves appointments
<img width="1536" height="1024" alt="UML" src="https://github.com/user-attachments/assets/f503fed9-dbf5-4e53-b81a-57af032fd38f" />



--> Class Diagram

User

Patient

Doctor

Appointment

Prescription

Bill
<img width="1536" height="1024" alt="use case" src="https://github.com/user-attachments/assets/c0f8f9c0-c1ec-4b17-93a5-4d6657fbd49a" />

-->sequence
<img width="1536" height="1024" alt="sequence" src="https://github.com/user-attachments/assets/1e085b90-c68f-4ed3-b723-5d519eb4b0f8" />


## Screenshots
 
### Home Page
![Home](screenshots/homepage.png)
<img width="1507" height="801" alt="Screenshot 2025-12-05 155230" src="https://github.com/user-attachments/assets/380622e4-6e85-4ebd-bbb7-eb582a0bc639" />

### Login Page
![Login](screenshots/login.png)
<img width="1892" height="988" alt="Screenshot 2025-12-05 155635" src="https://github.com/user-attachments/assets/4b320f65-1b26-41ef-9348-4a3c6398237e" />


### Doctor Dashboard
![Doctor Dashboard](screenshots/doctor_dashboard.png)
<img width="1908" height="982" alt="Screenshot 2025-12-05 155908" src="https://github.com/user-attachments/assets/addcea51-f417-404d-a486-7be13f3009dd" />



-> Future Enhancements

Email / SMS reminders

Online payment integration

OPD token system

Pharmacy module

Author

Swathi G
PES Hospital Management System
