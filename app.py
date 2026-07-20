from flask import Flask, render_template, request, session
from flask_migrate import Migrate
from config import Config
from models import db, Trip, Seat
from routes.operator import operator

app = Flask(__name__)

app.secret_key = "BUSSGO_SECRET_KEY"

# Load Configuration
app.config.from_object(Config)

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

    from_city = request.args.get("from_city")
    to_city = request.args.get("to_city")

    trips = Trip.query.filter_by(
        from_city=from_city,
        to_city=to_city
    ).all()

    return render_template(
        "search.html",
        trips=trips,
        from_city=from_city,
        to_city=to_city
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