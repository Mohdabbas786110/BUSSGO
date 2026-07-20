from datetime import datetime
from . import db


class Trip(db.Model):
    __tablename__ = "trips"

    id = db.Column(db.Integer, primary_key=True)

    # Bus
    bus_id = db.Column(
        db.Integer,
        db.ForeignKey("buses.id"),
        nullable=False
    )

    # Route
    from_city = db.Column(
        db.String(100),
        nullable=False
    )

    to_city = db.Column(
        db.String(100),
        nullable=False
    )

    boarding_point = db.Column(
        db.String(150),
        nullable=False
    )

    dropping_point = db.Column(
        db.String(150),
        nullable=False
    )

    # Journey
    journey_date = db.Column(
        db.Date,
        nullable=False
    )

    departure_time = db.Column(
        db.Time,
        nullable=False
    )

    arrival_time = db.Column(
        db.Time,
        nullable=False
    )

    # Fare
    fare = db.Column(
        db.Integer,
        nullable=False
    )

    # Seats
    total_seats = db.Column(
        db.Integer,
        default=40
    )

    available_seats = db.Column(
        db.Integer,
        default=40
    )

    # Trip Status
    status = db.Column(
        db.String(20),
        default="Scheduled"
    )

    # Created Time
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Relationship
    bus = db.relationship(
        "Bus",
        backref="trips"
    )

    def __repr__(self):
        return (
            f"<Trip {self.from_city} -> "
            f"{self.to_city} ({self.journey_date})>"
        )