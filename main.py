# main.py

from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import datetime   # ✅ ADD THIS LINE

from models import db, User, Doctors, Patients, Trigr

app = Flask(__name__)
app.secret_key = "hmsprojects"

# DATABASE CONFIG
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hospital.db"
db.init_app(app)

# LOGIN MANAGER
login_manager = LoginManager(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# ---------------------------------------------------
# AUTO AVAILABILITY CHECK FUNCTION
# ---------------------------------------------------
def get_doctor_availability(doctorname):
    count = Patients.query.filter_by(dept=doctorname).count()
    if count >= 5:
        return "Not Available"
    return "Available"

# ---------------------------
# HOME PAGE
# ---------------------------
@app.route("/")
@app.route("/")
def index():
    total_doctors = Doctors.query.count()
    total_patients = Patients.query.count()

    today = datetime.date.today().isoformat()
    todays = Patients.query.filter_by(date=today).count()

    return render_template("index.html",total_doctors=total_doctors,total_patients=total_patients,todays=todays)



# ---------------------------
# SIGNUP
# ---------------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        usertype = request.form["usertype"]
        email = request.form["email"]
        password = request.form["password"]

        if User.query.filter_by(email=email).first():
            flash("Email exists!", "danger")
            return redirect("/signup")

        user = User(
            username=username,
            usertype=usertype,
            email=email,
            password=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()

        flash("Signup successful!", "success")
        return redirect("/login")

    return render_template("signup.html")


# ---------------------------
# LOGIN
# ---------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Logged in!", "primary")
            return redirect("/")
        else:
            flash("Invalid credentials!", "danger")

    return render_template("login.html")


# ---------------------------
# LOGOUT
# ---------------------------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out!", "warning")
    return redirect("/login")


# ---------------------------
# ADD DOCTOR
# ---------------------------
@app.route("/doctors", methods=["GET", "POST"])
@login_required
def doctor_add():
    if request.method == "POST":
        email = request.form["email"]
        name = request.form["doctorname"]
        dept = request.form["dept"]

        d = Doctors(email=email, doctorname=name, dept=dept)
        db.session.add(d)
        db.session.commit()

        flash("Doctor added!", "success")

    return render_template("doctor.html")

# ---------------------------
# DOCTOR LIST (AUTO AVAILABILITY)
# ---------------------------
# ---------------------------
# DOCTOR LIST (AUTO AVAILABILITY + PATIENT COUNT + COLOR BADGE)
# ---------------------------
@app.route("/doctor-list")
@login_required
def doctor_list():
    docs = Doctors.query.all()

    for d in docs:
        # Auto-availability based on number of patients
        d.availability = get_doctor_availability(d.dept)

        # Count patient appointments for this doctor/department
        d.patient_count = Patients.query.filter_by(dept=d.dept).count()

        # Assign color based on patient load
        if d.patient_count <= 2:
            d.badge_color = "success"   # Green
        elif d.patient_count <= 4:
            d.badge_color = "warning"   # Yellow
        else:
            d.badge_color = "danger"    # Red

    db.session.commit()
    return render_template("doctor_list.html", doctors=docs)


# ---------------------------
# PATIENT BOOKING
# ---------------------------
@app.route("/patients", methods=["GET", "POST"])
@login_required
def patients():
    doctors = Doctors.query.all()

    if request.method == "POST":
        number = request.form["number"]

        if len(number) != 10:
            flash("Phone must be 10 digits", "danger")
            return render_template("patient.html", doct=doctors)

        p = Patients(
            email=request.form["email"],
            name=request.form["name"],
            gender=request.form["gender"],
            slot=request.form["slot"],
            disease=request.form["disease"],
            time=request.form["time"],
            date=request.form["date"],
            dept=request.form["dept"],
            number=number
        )
        db.session.add(p)
        db.session.commit()

        flash("Appointment booked!", "success")

    return render_template("patient.html", doct=doctors)


# ---------------------------
# SEARCH DOCTOR (FIXED ✔)
# ---------------------------
@app.route("/check_doctor", methods=["POST"])
@login_required
def check_doctor():
    q = request.form.get("search", "").strip()

    if not q:
        flash("Please enter text to search.", "warning")
        return redirect("/doctor-list")

    # CASE-INSENSITIVE SEARCH FOR NAME AND DEPARTMENT
    doctor = Doctors.query.filter(
        (Doctors.doctorname.ilike(f"%{q}%")) |
        (Doctors.dept.ilike(f"%{q}%"))
    ).first()

    if doctor:
        flash(f"Doctor Available: {doctor.doctorname} | Dept: {doctor.dept}", "success")
        return redirect(f"/doctor-schedule/{doctor.did}")

    flash("No doctor found by that name or department.", "danger")
    return redirect("/doctor-list")


# ---------------------------
# VIEW BOOKINGS
# ---------------------------
@app.route("/bookings")
@login_required
def bookings():
    if current_user.usertype == "Doctor":
        data = Patients.query.all()
    else:
        data = Patients.query.filter_by(email=current_user.email)

    return render_template("booking.html", query=data)


# ---------------------------
# BILLING SAFE FALLBACK
# ---------------------------
@app.route("/bill")
def bill_default():
    flash("Please open Bill from a patient's row!", "warning")
    return redirect("/bookings")


# ---------------------------
# BILLING PAGE
# ---------------------------
@app.route("/bill/<int:pid>")
@login_required
def bill(pid):
    patient = Patients.query.get(pid)

    if not patient:
        flash("Patient not found!", "danger")
        return redirect("/bookings")

    doctor_fee = 500
    treatment_fee = 700

    return render_template(
        "bill.html",
        patient=patient,
        doctor_fee=doctor_fee,
        treatment_fee=treatment_fee,
        total=doctor_fee + treatment_fee
    )


@app.route("/bill-result", methods=["POST"])
@login_required
def bill_result():
    doctor_fee = int(request.form["doctor_fee"])
    treatment_fee = int(request.form["treatment_fee"])
    total = doctor_fee + treatment_fee

    return render_template(
        "bill_result.html",
        name=request.form["name"],
        disease=request.form["disease"],
        date=request.form["date"],
        doctor_fee=doctor_fee,
        treatment_fee=treatment_fee,
        total=total
    )
# ---------------------------
# DELETE Booking
# ---------------------------
@app.route("/delete/<int:pid>")
@login_required
def delete(pid):
    patient = Patients.query.get(pid)
    if not patient:
        flash("Record not found!", "danger")
        return redirect("/bookings")

    db.session.delete(patient)
    db.session.commit()
    flash("Booking deleted successfully!", "success")
    return redirect("/bookings")


@app.route("/update/<int:pid>", methods=["POST"])
@login_required
def update(pid):
    patient = Patients.query.get(pid)
    if not patient:
        flash("Record not found!", "danger")
        return redirect("/bookings")

    patient.name = request.form["name"]
    patient.disease = request.form["disease"]
    patient.date = request.form["date"]
    patient.time = request.form["time"]
    db.session.commit()
    flash("Record updated successfully!", "success")
    return redirect("/bookings")
@app.route("/edit/<int:pid>")
@login_required
def edit(pid):
    patient = Patients.query.get(pid)
    if not patient:
        flash("Record not found!", "danger")
        return redirect("/bookings")
    return render_template("edit.html", patient=patient)

@app.route("/doctor/availability/<int:did>/<status>")
@login_required
def doctor_availability(did, status):
    doc = Doctors.query.get(did)

    if not doc:
        flash("Doctor not found!", "danger")
        return redirect("/doctor-list")

    doc.availability = status
    db.session.commit()

    flash(f"Doctor marked as {status}", "success")
    return redirect("/doctor-list")
def get_doctor_availability(doctorname):
    count = Patients.query.filter_by(dept=doctorname).count()
    if count >= 5:
        return "Not Available"
    return "Available"

# helper
def is_doctor():
    return current_user.is_authenticated and current_user.usertype == "Doctor"

def is_admin():
    return current_user.is_authenticated and current_user.usertype == "Admin"

def is_patient():
    return current_user.is_authenticated and current_user.usertype == "Patient"


@app.route("/doctor/dashboard")
@login_required
def doctor_dashboard():
    if not is_doctor():
        flash("Only doctors can access this page", "danger")
        return redirect("/")

    # find doctor entry for this logged-in doctor via email
    doc = Doctors.query.filter_by(email=current_user.email).first()
    if not doc:
        flash("Doctor profile not found", "danger")
        return redirect("/")

    # Today's appointments (date in same format as Patients.date)
    today = datetime.date.today().isoformat()
    todays = Patients.query.filter_by(dept=doc.doctorname, date=today).all()

    # all patients for this doctor
    patients = Patients.query.filter_by(dept=doc.doctorname).all()

    schedules = DoctorSchedule.query.filter_by(doctor_id=doc.did).all()

    return render_template("doctor_dashboard.html",doc=doc, todays=todays, patients=patients, schedules=schedules)

@app.route("/prescribe/<int:pid>", methods=["GET", "POST"])
@login_required
def prescribe(pid):
    if current_user.usertype != "Doctor":
        flash("Only doctors can add prescriptions!", "danger")
        return redirect("/")

    patient = Patients.query.get(pid)
    doctor = Doctors.query.filter_by(email=current_user.email).first()

    if request.method == "POST":
        pres = Prescription(
            patient_id=pid,
            doctor_id=doctor.did,
            details=request.form["details"],
            date=datetime.date.today().isoformat()
        )
        db.session.add(pres)
        db.session.commit()
        flash("Prescription added!", "success")
        return redirect("/bookings")

    return render_template("prescribe.html", patient=patient)

@app.route("/prescriptions/<int:pid>")
@login_required
def view_prescriptions(pid):
    data = Prescription.query.filter_by(patient_id=pid).all()
    patient = Patients.query.get(pid)
    return render_template("view_prescriptions.html", data=data, patient=patient)


@app.route("/upload_report/<int:pid>", methods=["GET", "POST"])
@login_required
def upload_report(pid):
    patient = Patients.query.get(pid)

    if request.method == "POST":
        file = request.files["report"]

        if file:
            filename = file.filename
            file.save("static/reports/" + filename)

            r = Reports(
                patient_id=pid,
                filename=filename,
                date=datetime.date.today().isoformat()
            )
            db.session.add(r)
            db.session.commit()

            flash("Report uploaded!", "success")
            return redirect(f"/reports/{pid}")

    return render_template("upload_report_form.html", patient=patient)

@app.route("/reports/<int:pid>")
@login_required
def reports(pid):
    data = Reports.query.filter_by(patient_id=pid).all()
    patient = Patients.query.get(pid)
    return render_template("reports.html", data=data, patient=patient)

# ---------------------------
# REGISTER BLUEPRINT
# ---------------------------
from features import features_bp
app.register_blueprint(features_bp)


# ---------------------------
# RUN SERVER
# ---------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
