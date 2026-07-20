from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for
)

operator = Blueprint("operator", __name__)


# -----------------------------
# Dashboard
# -----------------------------
@operator.route("/operator/dashboard")
def dashboard():
    return render_template("operator_dashboard.html")


# -----------------------------
# Add Bus
# -----------------------------
@operator.route("/operator/add-bus")
def add_bus():
    return render_template("add_bus.html")


# -----------------------------
# STEP 1
# -----------------------------
@operator.route("/register-bus/step1", methods=["GET", "POST"])
def register_step1():

    if request.method == "POST":

        session["operator"] = {
            "company_name": request.form.get("company_name"),
            "owner_name": request.form.get("owner_name"),
            "mobile": request.form.get("mobile"),
            "address": request.form.get("address")
        }

        return redirect(url_for("operator.register_step2"))

    return render_template("register_bus_step1.html")


# -----------------------------
# STEP 2
# -----------------------------
@operator.route("/register-bus/step2", methods=["GET", "POST"])
def register_step2():

    if request.method == "POST":

        session["bus"] = {
            "bus_name": request.form.get("bus_name"),
            "bus_number": request.form.get("bus_number"),
            "bus_type": request.form.get("bus_type"),
            "total_seats": request.form.get("total_seats")
        }

        return redirect(url_for("operator.register_step3"))

    return render_template("register_bus_step2.html")