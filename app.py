import os

from flask import Flask, render_template, request, session, redirect, url_for
from flask_migrate import Migrate
from config import Config
from models import db, Trip, Seat, Booking, User
from sqlalchemy import func
from routes.operator import operator
from routes.auth.auth import auth
from datetime import datetime, timedelta

app = Flask(__name__)

# Load Configuration
app.config.from_object(Config)

# Create upload folder automatically
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Initialize Database
db.init_app(app)

# Flask-Migrate
migrate = Migrate(app, db)

# Register Blueprints
app.register_blueprint(operator)
app.register_blueprint(auth)

# Home Route
@app.route("/")
def home():
    return render_template("index.html")

# ==========================================
# SEARCH ROUTE
# ==========================================

@app.route("/search")
def search():

    from_city = request.args.get(
        "from_city",
        ""
    ).strip()

    to_city = request.args.get(
        "to_city",
        ""
    ).strip()

    journey_date = request.args.get(
        "journey_date",
        ""
    ).strip()


    # ==========================================
    # CHECK CITY INPUT
    # ==========================================

    if not from_city or not to_city:

        return render_template(
            "search.html",
            trips=[],
            from_city=from_city,
            to_city=to_city,
            journey_date=journey_date
        )


    # ==========================================
    # SEARCH BUSES
    # ==========================================

    query = Trip.query.filter(

        func.lower(
            Trip.from_city
        ) == from_city.lower(),

        func.lower(
            Trip.to_city
        ) == to_city.lower()

    )


    # Get matching trips
    trips = query.all()


    # ==========================================
    # AI BUS RECOMMENDATION
    # ==========================================

    if trips:

        # --------------------------------------
        # Prefer scheduled buses
        # --------------------------------------

        scheduled_trips = [

            trip
            for trip in trips

            if trip.status
            and trip.status.lower() == "scheduled"

        ]

        if scheduled_trips:

            trips = scheduled_trips


        # --------------------------------------
        # Fare range
        # --------------------------------------

        max_fare = max(
            trip.fare
            for trip in trips
        )

        min_fare = min(
            trip.fare
            for trip in trips
        )


        # --------------------------------------
        # Seat availability range
        # --------------------------------------

        max_seats = max(

            trip.available_seats or 0

            for trip in trips

        )


        # --------------------------------------
        # Calculate journey duration
        # --------------------------------------

        for trip in trips:

            departure = datetime.combine(

                datetime.today(),

                trip.departure_time

            )

            arrival = datetime.combine(

                datetime.today(),

                trip.arrival_time

            )


            # Overnight journey
            if arrival < departure:

                arrival += timedelta(
                    days=1
                )


            trip.duration_minutes = (

                arrival - departure

            ).total_seconds() / 60


        # --------------------------------------
        # Duration range
        # --------------------------------------

        max_duration = max(

            trip.duration_minutes

            for trip in trips

        )

        min_duration = min(

            trip.duration_minutes

            for trip in trips

        )


        # --------------------------------------
        # Calculate AI score for each bus
        # --------------------------------------

        for trip in trips:


            # ==================================
            # FARE SCORE
            # ==================================

            if max_fare == min_fare:

                fare_score = 100

            else:

                fare_score = (

                    (
                        max_fare
                        -
                        trip.fare
                    )

                    /

                    (
                        max_fare
                        -
                        min_fare
                    )

                ) * 100


            # ==================================
            # SEAT SCORE
            # ==================================

            available_seats = (
                trip.available_seats or 0
            )


            if max_seats == 0:

                seat_score = 0

            else:

                seat_score = (

                    available_seats
                    /
                    max_seats

                ) * 100


            # ==================================
            # JOURNEY DURATION SCORE
            # ==================================

            if max_duration == min_duration:

                duration_score = 100

            else:

                duration_score = (

                    (
                        max_duration
                        -
                        trip.duration_minutes
                    )

                    /

                    (
                        max_duration
                        -
                        min_duration
                    )

                ) * 100


            # ==================================
            # FINAL AI SCORE
            # ==================================

            trip.ai_score = round(

                (fare_score * 0.40)

                +

                (seat_score * 0.25)

                +

                (duration_score * 0.35)

            )


            trip.ai_recommended = False


        # ==================================
        # SORT BY AI SCORE
        # ==================================

        trips.sort(

            key=lambda trip:
            trip.ai_score,

            reverse=True

        )


        # ==================================
        # BEST BUS RECOMMENDATION
        # ==================================

        if trips:

            trips[0].ai_recommended = True


    # ==========================================
    # SHOW SEARCH RESULTS
    # ==========================================

    return render_template(

        "search.html",

        trips=trips,

        from_city=from_city,

        to_city=to_city,

        journey_date=journey_date

    )

# view seat
@app.route("/view-seats/<int:trip_id>")
def view_seats(trip_id):

    trip = Trip.query.get_or_404(trip_id)

    seats = Seat.query.filter_by(
        trip_id=trip.id
    ).all()

    if not seats:

        rows = ["A","B","C","D","E","F","G","H","I","J"]

        for row in rows:
            for number in range(1,5):

                seat = Seat(
                    trip_id=trip.id,
                    seat_number=f"{row}{number}"
                )

                db.session.add(seat)

        db.session.commit()

        seats = Seat.query.filter_by(
            trip_id=trip.id
        ).all()

    return render_template(
        "view_seats.html",
        trip=trip,
        seats=seats
    )


# ==========================================
# MULTIPLE SEAT BOOKING PAGE
# ==========================================

@app.route("/booking/<int:trip_id>/<seat_ids>")
def booking_page(trip_id, seat_ids):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    trip = Trip.query.get_or_404(trip_id)

    try:
        seat_id_list = [
            int(seat_id)
            for seat_id in seat_ids.split(",")
        ]
    except ValueError:
        return "Invalid seat selection.", 400

    if not seat_id_list:
        return "No seats selected.", 400

    if len(seat_id_list) > 6:
        return "Maximum 6 seats can be booked at a time.", 400

    seats = Seat.query.filter(
        Seat.id.in_(seat_id_list),
        Seat.trip_id == trip.id
    ).all()

    if len(seats) != len(seat_id_list):
        return "Invalid seat selection.", 400

    for seat in seats:

        if seat.is_booked:
            return (
                f"Sorry, seat {seat.seat_number} "
                f"has already been booked.",
                400
            )

    user = User.query.get_or_404(
        session["user_id"]
    )

    total_fare = len(seats) * trip.fare

    return render_template(
        "booking_confirmation.html",
        trip=trip,
        seats=seats,
        user=user,
        total_fare=total_fare
    )


## ==========================================
# CONFIRM MULTIPLE SEAT BOOKING
# ==========================================

@app.route(
    "/confirm-booking/<int:trip_id>/<seat_ids>",
    methods=["POST"]
)
def confirm_booking(trip_id, seat_ids):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    trip = Trip.query.get_or_404(trip_id)

    try:
        seat_id_list = [
            int(seat_id)
            for seat_id in seat_ids.split(",")
        ]
    except ValueError:
        return "Invalid seat selection.", 400

    if not seat_id_list:
        return "No seats selected.", 400

    if len(seat_id_list) > 6:
        return "Maximum 6 seats can be booked at a time.", 400

    seats = Seat.query.filter(
        Seat.id.in_(seat_id_list),
        Seat.trip_id == trip.id
    ).all()

    if len(seats) != len(seat_id_list):
        return "Invalid seat selection.", 400

    for seat in seats:

        if seat.is_booked:
            return (
                f"Sorry, seat {seat.seat_number} "
                f"has already been booked.",
                400
            )

    user = User.query.get_or_404(
        session["user_id"]
    )

    total_fare = len(seats) * trip.fare

    # Store selected seats temporarily
    session["pending_booking"] = {
        "trip_id": trip.id,
        "seat_ids": seat_id_list,
        "total_fare": total_fare
    }

    return render_template(
        "payment.html",
        trip=trip,
        seats=seats,
        user=user,
        total_fare=total_fare
    )

# ==========================================
# PROCESS DEMO PAYMENT
# ==========================================

@app.route(
    "/process-payment/<int:trip_id>",
    methods=["POST"]
)
def process_payment(trip_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    # Check pending booking
    pending_booking = session.get("pending_booking")

    if not pending_booking:
        return "No pending booking found.", 400

    # Verify trip
    if pending_booking.get("trip_id") != trip_id:
        return "Invalid payment request.", 400

    trip = Trip.query.get_or_404(trip_id)

    seat_id_list = pending_booking.get("seat_ids", [])

    if not seat_id_list:
        return "No seats selected.", 400

    # Maximum 6 seats
    if len(seat_id_list) > 6:
        return "Maximum 6 seats can be booked at a time.", 400

    # Get seats again from database
    seats = Seat.query.filter(
        Seat.id.in_(seat_id_list),
        Seat.trip_id == trip.id
    ).all()

    if len(seats) != len(seat_id_list):
        return "Invalid seat selection.", 400

    # Check if any seat was booked while payment was pending
    for seat in seats:

        if seat.is_booked:

            session.pop("pending_booking", None)

            return (
                f"Sorry, seat {seat.seat_number} "
                f"has already been booked.",
                400
            )

    # Get logged-in user
    user = User.query.get_or_404(
        session["user_id"]
    )

    # Get payment method
    payment_method = request.form.get(
        "payment_method",
        "Demo Payment"
    )

    # Calculate total fare again from database
    total_fare = len(seats) * trip.fare

    bookings = []

    # ==========================================
    # SIMULATED PAYMENT
    # ==========================================

    payment_successful = True

    if payment_successful:

        # Create booking for every selected seat
        for seat in seats:

            booking = Booking(
                trip_id=trip.id,
                user_id=user.id,
                passenger_name=user.full_name,
                passenger_mobile=user.mobile,
                seat_number=seat.seat_number,
                fare=trip.fare,
                payment_status="Paid",
                booking_status="Booked"
            )

            # Mark seat as booked
            seat.is_booked = True

            bookings.append(booking)

            db.session.add(booking)

        # Reduce available seats
        booked_count = len(seats)

        trip.available_seats = max(
            0,
            (trip.available_seats or 0) - booked_count
        )

        # Save everything
        db.session.commit()

        # Remove pending booking
        session.pop("pending_booking", None)

        # Payment completed successfully
        return render_template(
            "booking_success.html",
            bookings=bookings,
            trip=trip,
            total_fare=total_fare,
            payment_method=payment_method
        )

    return "Payment failed. Please try again.", 400

# ==========================================
# MY BOOKINGS
# ==========================================

@app.route("/my-bookings")
def my_bookings():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    bookings = Booking.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        Booking.booking_time.desc()
    ).all()

    return render_template(
        "my_bookings.html",
        bookings=bookings
    )

if __name__ == "__main__":
    app.run(debug=True)