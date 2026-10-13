from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from models import db, User
import re
import random

auth = Blueprint("auth", __name__)


# ==========================================
# REGISTER
# ==========================================

@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form.get(
            "full_name",
            ""
        ).strip()

        mobile = request.form.get(
            "mobile",
            ""
        ).strip()

        if not full_name or not mobile:

            flash(
                "Please fill all fields.",
                "danger"
            )

            return render_template(
                "register.html"
            )

        if not re.fullmatch(
            r"[0-9]{10}",
            mobile
        ):

            flash(
                "Please enter a valid 10-digit mobile number.",
                "danger"
            )

            return render_template(
                "register.html"
            )

        user = User.query.filter_by(
            mobile=mobile
        ).first()

        if user:

            flash(
                "Mobile number already registered. Please login.",
                "warning"
            )

            return redirect(
                url_for("auth.login")
            )

        # Create user
        user = User(
            full_name=full_name,
            mobile=mobile,
            role="passenger",
            is_verified=True
        )

        db.session.add(user)
        db.session.commit()

        # Login after registration
        session["user_id"] = user.id
        session["user_name"] = user.full_name
        session["user_mobile"] = user.mobile

        flash(
            "Registration successful!",
            "success"
        )

        return redirect(
            url_for("home")
        )

    return render_template(
        "register.html"
    )


# ==========================================
# LOGIN - SEND OTP
# ==========================================

@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        mobile = request.form.get(
            "mobile",
            ""
        ).strip()

        if not re.fullmatch(
            r"[0-9]{10}",
            mobile
        ):

            flash(
                "Please enter a valid 10-digit mobile number.",
                "danger"
            )

            return render_template(
                "login.html"
            )

        user = User.query.filter_by(
            mobile=mobile
        ).first()

        if not user:

            flash(
                "Mobile number not registered. Please register first.",
                "warning"
            )

            return redirect(
                url_for("auth.register")
            )

        # Generate 6-digit OTP
        otp = str(
            random.randint(
                100000,
                999999
            )
        )

        # Store OTP temporarily in session
        session["login_otp"] = otp
        session["login_mobile"] = mobile

        # Demo OTP
        print(
            "================================"
        )

        print(
            f"BUSSGO DEMO OTP: {otp}"
        )

        print(
            "================================"
        )

        return render_template(
            "verify_otp.html",
            mobile=mobile,
            demo_otp=otp
        )

    return render_template(
        "login.html"
    )


# ==========================================
# VERIFY OTP
# ==========================================

@auth.route(
    "/verify-otp",
    methods=["POST"]
)
def verify_otp():

    entered_otp = request.form.get(
        "otp",
        ""
    ).strip()

    saved_otp = session.get(
        "login_otp"
    )

    mobile = session.get(
        "login_mobile"
    )

    if not saved_otp or not mobile:

        flash(
            "OTP session expired. Please login again.",
            "danger"
        )

        return redirect(
            url_for("auth.login")
        )

    if entered_otp != saved_otp:

        flash(
            "Invalid OTP. Please try again.",
            "danger"
        )

        return render_template(
            "verify_otp.html",
            mobile=mobile,
            demo_otp=saved_otp
        )

    # Get user
    user = User.query.filter_by(
        mobile=mobile
    ).first()

    if not user:

        flash(
            "User not found.",
            "danger"
        )

        return redirect(
            url_for("auth.login")
        )

    # Login user
    session["user_id"] = user.id
    session["user_name"] = user.full_name
    session["user_mobile"] = user.mobile

    # Remove OTP after successful verification
    session.pop(
        "login_otp",
        None
    )

    session.pop(
        "login_mobile",
        None
    )

    flash(
        "OTP verified. Login successful!",
        "success"
    )

    return redirect(
        url_for("home")
    )


# ==========================================
# LOGOUT
# ==========================================

@auth.route("/logout")
def logout():

    session.clear()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(
        url_for("home")
    )