from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from models import db, Operator, Bus, Trip

from datetime import datetime

from werkzeug.utils import secure_filename

import os


operator = Blueprint("operator", __name__)


# =========================================================
# OPERATOR DASHBOARD
# =========================================================

@operator.route("/operator/dashboard")
def dashboard():

    return render_template(
        "operator_dashboard.html"
    )


# =========================================================
# ADD BUS
# =========================================================

@operator.route("/operator/add-bus")
def add_bus():

    return render_template(
        "add_bus.html"
    )


# =========================================================
# CREATE TRIP
# =========================================================

@operator.route(
    "/operator/add-trip",
    methods=["GET", "POST"]
)
def add_trip():

    if request.method == "POST":

        from_city = request.form.get(
            "from_city",
            ""
        ).strip()

        to_city = request.form.get(
            "to_city",
            ""
        ).strip()

        boarding_point = request.form.get(
            "boarding_point",
            ""
        ).strip()

        dropping_point = request.form.get(
            "dropping_point",
            ""
        ).strip()

        journey_date = request.form.get(
            "journey_date",
            ""
        ).strip()

        departure_time = request.form.get(
            "departure_time",
            ""
        ).strip()

        arrival_time = request.form.get(
            "arrival_time",
            ""
        ).strip()

        fare = request.form.get(
            "fare",
            ""
        ).strip()

        bus_id = request.form.get(
            "bus_id",
            ""
        ).strip()


        # -----------------------------------------
        # VALIDATION
        # -----------------------------------------

        if not all([
            from_city,
            to_city,
            boarding_point,
            dropping_point,
            journey_date,
            departure_time,
            arrival_time,
            fare,
            bus_id
        ]):

            flash(
                "Please fill all trip details.",
                "danger"
            )

            buses = Bus.query.all()

            return render_template(
                "add_trip.html",
                buses=buses
            )


        try:

            bus = Bus.query.get_or_404(
                int(bus_id)
            )

            trip = Trip(

                bus_id=bus.id,

                from_city=from_city,

                to_city=to_city,

                boarding_point=boarding_point,

                dropping_point=dropping_point,

                journey_date=datetime.strptime(
                    journey_date,
                    "%Y-%m-%d"
                ).date(),

                departure_time=datetime.strptime(
                    departure_time,
                    "%H:%M"
                ).time(),

                arrival_time=datetime.strptime(
                    arrival_time,
                    "%H:%M"
                ).time(),

                fare=int(fare),

                total_seats=bus.total_seats,

                available_seats=bus.total_seats

            )


            db.session.add(trip)

            db.session.commit()


            flash(
                "Trip created successfully!",
                "success"
            )

            return redirect(
                url_for(
                    "operator.dashboard"
                )
            )


        except Exception as e:

            db.session.rollback()

            print(
                "CREATE TRIP ERROR:",
                e
            )

            flash(
                "Trip creation failed. Please check the terminal.",
                "danger"
            )


    # -----------------------------------------
    # SHOW BUSES
    # -----------------------------------------

    buses = Bus.query.all()

    return render_template(
        "add_trip.html",
        buses=buses
    )


# =========================================================
# REGISTER BUS - STEP 1
# =========================================================

@operator.route(
    "/register-bus/step1",
    methods=["GET", "POST"]
)
def register_step1():

    if request.method == "POST":

        session["operator"] = {

            "company_name":
                request.form.get(
                    "operator_name"
                ),

            "owner_name":
                request.form.get(
                    "owner_name"
                ),

            "mobile":
                request.form.get(
                    "mobile"
                ),

            "address":
                request.form.get(
                    "address"
                )

        }

        print(
            session["operator"]
        )

        return redirect(
            url_for(
                "operator.register_step2"
            )
        )


    return render_template(
        "register_bus_step1.html"
    )


# =========================================================
# REGISTER BUS - STEP 2
# =========================================================

@operator.route(
    "/register-bus/step2",
    methods=["GET", "POST"]
)
def register_step2():

    if request.method == "POST":

        session["bus"] = {

            "bus_name":
                request.form.get(
                    "bus_name"
                ),

            "bus_number":
                request.form.get(
                    "bus_number"
                ),

            "bus_type":
                request.form.get(
                    "bus_type"
                ),

            "total_seats":
                request.form.get(
                    "total_seats"
                )

        }

        return redirect(
            url_for(
                "operator.register_step3"
            )
        )


    return render_template(
        "register_bus_step2.html"
    )


# =========================================================
# REGISTER BUS - STEP 3
# =========================================================

@operator.route(
    "/register-bus/step3",
    methods=["GET", "POST"]
)
def register_step3():

    if request.method == "POST":

        session["trip"] = {

            "from_city":
                request.form.get(
                    "from_city"
                ),

            "to_city":
                request.form.get(
                    "to_city"
                ),

            "boarding_point":
                request.form.get(
                    "boarding_point"
                ),

            "dropping_point":
                request.form.get(
                    "dropping_point"
                ),

            "journey_date":
                request.form.get(
                    "journey_date"
                ),

            "departure_time":
                request.form.get(
                    "departure_time"
                ),

            "arrival_time":
                request.form.get(
                    "arrival_time"
                ),

            "fare":
                request.form.get(
                    "fare"
                )

        }

        return redirect(
            url_for(
                "operator.register_step4"
            )
        )


    return render_template(
        "register_bus_step3.html"
    )


# =========================================================
# REGISTER BUS - STEP 4
# =========================================================

@operator.route(
    "/register-bus/step4",
    methods=["GET", "POST"]
)
def register_step4():

    if request.method == "POST":

        session["staff"] = {

            "driver_name":
                request.form.get(
                    "driver_name"
                ),

            "driver_mobile":
                request.form.get(
                    "driver_mobile"
                ),

            "conductor_name":
                request.form.get(
                    "conductor_name"
                ),

            "conductor_mobile":
                request.form.get(
                    "conductor_mobile"
                )

        }

        return redirect(
            url_for(
                "operator.register_step5"
            )
        )


    return render_template(
        "register_bus_step4.html"
    )


# =========================================================
# REGISTER BUS - STEP 5
# =========================================================

@operator.route(
    "/register-bus/step5",
    methods=["GET"]
)
def register_step5():

    return render_template(
        "register_bus_step5.html"
    )


# =========================================================
# REGISTER BUS - SUCCESS
# =========================================================

@operator.route(
    "/register-bus/success"
)
def register_success():

    return """
    <!DOCTYPE html>

    <html>

    <head>

        <title>BUSSGO - Success</title>

        <style>

            body {
                font-family: Arial;
                text-align: center;
                padding-top: 100px;
            }

            h2 {
                color: green;
            }

            a {
                text-decoration: none;
                color: white;
                background: #dc3545;
                padding: 10px 20px;
                border-radius: 6px;
            }

        </style>

    </head>

    <body>

        <h2>
            ✅ Bus Registered Successfully
        </h2>

        <br>

        <a href="/">
            Go Home
        </a>

    </body>

    </html>
    """


# =========================================================
# REGISTER BUS - SUBMIT
# =========================================================

@operator.route(
    "/register-bus/submit",
    methods=["POST"]
)
def register_submit():

    print(
        "Operator:",
        session.get("operator")
    )

    print(
        "Bus:",
        session.get("bus")
    )

    print(
        "Trip:",
        session.get("trip")
    )

    print(
        "Staff:",
        session.get("staff")
    )


    operator_data = session.get(
        "operator"
    )

    bus_data = session.get(
        "bus"
    )

    trip_data = session.get(
        "trip"
    )

    staff_data = session.get(
        "staff"
    )


    # -----------------------------------------
    # CHECK SESSION
    # -----------------------------------------

    if (
        not operator_data
        or not bus_data
        or not trip_data
    ):

        return (
            "Registration session expired. "
            "Please register again."
        )


    # -----------------------------------------
    # CHECK DUPLICATE OPERATOR
    # -----------------------------------------

    existing_operator = Operator.query.filter_by(
        mobile=operator_data["mobile"]
    ).first()


    if existing_operator:

        flash(
            "This mobile number is already registered "
            "as an operator. Please use another "
            "mobile number.",
            "warning"
        )

        return redirect(
            url_for(
                "operator.register_step1"
            )
        )


    # -----------------------------------------
    # CREATE UPLOAD FOLDER
    # -----------------------------------------

    upload_folder = os.path.join(
        "static",
        "uploads",
        "buses"
    )

    os.makedirs(
        upload_folder,
        exist_ok=True
    )


    # -----------------------------------------
    # BUS PHOTO
    # -----------------------------------------

    photo = request.files.get(
        "bus_photo"
    )

    filename = None


    if photo and photo.filename:

        filename = secure_filename(
            photo.filename
        )

        photo.save(
            os.path.join(
                upload_folder,
                filename
            )
        )


    try:

        # -----------------------------------------
        # SAVE OPERATOR
        # -----------------------------------------

        new_operator = Operator(

            company_name=
                operator_data["company_name"],

            owner_name=
                operator_data["owner_name"],

            mobile=
                operator_data["mobile"],

            address=
                operator_data["address"]

        )


        db.session.add(
            new_operator
        )

        db.session.flush()


        # -----------------------------------------
        # SAVE BUS
        # -----------------------------------------

        bus = Bus(

            operator_id=
                new_operator.id,

            bus_name=
                bus_data["bus_name"],

            bus_number=
                bus_data["bus_number"],

            bus_type=
                bus_data["bus_type"],

            total_seats=
                int(
                    bus_data["total_seats"]
                ),

            bus_photo=
                filename

        )


        db.session.add(
            bus
        )

        db.session.flush()


        # -----------------------------------------
        # SAVE TRIP
        # -----------------------------------------

        trip = Trip(

            bus_id=
                bus.id,

            from_city=
                trip_data["from_city"],

            to_city=
                trip_data["to_city"],

            boarding_point=
                trip_data["boarding_point"],

            dropping_point=
                trip_data["dropping_point"],

            journey_date=
                datetime.strptime(
                    trip_data["journey_date"],
                    "%Y-%m-%d"
                ).date(),

            departure_time=
                datetime.strptime(
                    trip_data["departure_time"],
                    "%H:%M"
                ).time(),

            arrival_time=
                datetime.strptime(
                    trip_data["arrival_time"],
                    "%H:%M"
                ).time(),

            fare=
                int(
                    trip_data["fare"]
                ),

            total_seats=
                int(
                    bus_data["total_seats"]
                ),

            available_seats=
                int(
                    bus_data["total_seats"]
                )

        )


        db.session.add(
            trip
        )


        # -----------------------------------------
        # COMMIT
        # -----------------------------------------

        db.session.commit()


        # -----------------------------------------
        # CLEAR REGISTRATION SESSION
        # -----------------------------------------

        session.pop(
            "operator",
            None
        )

        session.pop(
            "bus",
            None
        )

        session.pop(
            "trip",
            None
        )

        session.pop(
            "staff",
            None
        )


        return redirect(
            url_for(
                "operator.register_success"
            )
        )


    except Exception as e:

        db.session.rollback()

        print(
            "BUS REGISTRATION ERROR:",
            e
        )

        return (
            "Bus registration failed. "
            "Please check the terminal "
            "for the error.",
            500
        )