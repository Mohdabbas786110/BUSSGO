import os

from flask import Flask, render_template, request, session
from flask_migrate import Migrate
from config import Config
from models import db, Trip, Seat
from sqlalchemy import func
from routes.operator import operator
from datetime import datetime

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

# Home Route
@app.route("/")
def home():
    return render_template("index.html")

# Search Route
@app.route("/search")
def search():

    from_city = request.args.get("from_city", "").strip()
    to_city = request.args.get("to_city", "").strip()
    journey_date = request.args.get("journey_date", "").strip()

    # Agar user ne city select nahi ki
    if not from_city or not to_city:
        return render_template(
            "search.html",
            trips=[],
            from_city=from_city,
            to_city=to_city,
            journey_date=journey_date
        )

    # City ke basis par search (case-insensitive)
    trips = Trip.query.filter(
        func.lower(Trip.from_city) == from_city.lower(),
        func.lower(Trip.to_city) == to_city.lower()
    ).all()

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

if __name__ == "__main__":
    app.run(debug=True)