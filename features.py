# features.py

from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from models import db, Patients, Doctors, Trigr, DoctorSchedule

features_bp = Blueprint("features_bp", __name__)


# ---------------------------------------
# 0. SAFE FALLBACK ROUTE FOR /schedule (fixes 404)
# ---------------------------------------
@features_bp.route("/schedule")
def schedule_default():
    flash("Please select a doctor to set or view schedule.", "warning")
    return redirect("/doctor-list")


# ---------------------------------------
# 1. APPOINTMENT HISTORY
# ---------------------------------------
@features_bp.route("/history")
@login_required
def history():
    if current_user.usertype == "Doctor":
        data = Patients.query.all()
    else:
        data = Patients.query.filter_by(email=current_user.email).all()

    return render_template("history.html", data=data)


# ---------------------------------------
# 2. DOCTOR LIST PAGE
# ---------------------------------------
@features_bp.route("/doctor-list")
@login_required
def doctor_list():
    docs = Doctors.query.all()
    return render_template("doctor_list.html", doctors=docs)


# ---------------------------------------
# 3. SET DOCTOR SCHEDULE (doctor uploads timings)
# ---------------------------------------
@features_bp.route("/schedule/<int:did>", methods=["GET", "POST"])
@login_required
def schedule(did):
    doc = Doctors.query.get(did)

    if not doc:
        flash("Doctor not found!", "danger")
        return redirect("/doctor-list")

    # Save schedule
    if request.method == "POST":
        sch = DoctorSchedule(
            doctor_id=did,
            date=request.form.get("date"),
            start_time=request.form.get("start"),
            end_time=request.form.get("end")
        )
        db.session.add(sch)
        db.session.commit()

        flash("Schedule saved successfully!", "success")
        return redirect(f"/schedule/{did}")

    # Fetch doctor schedules
    schedules = DoctorSchedule.query.filter_by(doctor_id=did).all()

    return render_template("schedule.html", doc=doc, schedules=schedules)


# ---------------------------------------
# 4. VIEW DOCTOR SCHEDULE (patient/doctor view)
# ---------------------------------------
@features_bp.route("/doctor-schedule/<int:did>")
@login_required
def doctor_schedule(did):
    doc = Doctors.query.get(did)
    schedules = DoctorSchedule.query.filter_by(doctor_id=did).all()
    return render_template("doctor_schedule.html", doc=doc, schedules=schedules)


# ---------------------------------------
# 5. ADMIN DASHBOARD
# ---------------------------------------
@features_bp.route("/admin")
@login_required
def admin():
    if current_user.usertype != "Doctor":
        flash("Only admin/doctor can access this page.", "danger")
        return redirect("/")

    stats = {
        "total_patients": Patients.query.count(),
        "total_doctors": Doctors.query.count(),
        "total_appointments": Patients.query.count()
    }

    return render_template("admin.html", stats=stats)


# ---------------------------------------
# 6. UPLOAD MEDICAL REPORT
# ---------------------------------------
@features_bp.route("/upload_report", methods=["GET", "POST"])
@login_required
def upload_report():
    if request.method == "POST":
        file = request.files.get("report")

        if not file:
            flash("Please upload a valid report file!", "danger")
        else:
            file.save("static/reports/" + file.filename)
            flash("Report uploaded successfully!", "success")

    return render_template("upload_report.html")
