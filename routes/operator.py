from flask import Blueprint, render_template

operator = Blueprint("operator", __name__)


@operator.route("/operator/dashboard")
def dashboard():
    return render_template("operator_dashboard.html")

@operator.route("/operator/add-bus", methods=["GET", "POST"])
def add_bus():

    return render_template("add_bus.html")