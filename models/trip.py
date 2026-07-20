from datetime import datetime
from . import db


class Trip(db.Model):
    __tablename__ = "trips"

    id = db.Column(db.Integer, primary_key=True)

    bus_id = db.Column(
        db.Integer,
        db.ForeignKey("buses.id"),
        nullable=False
    )

    from_city = db.Column(
        db.String(100),
        nullable=False
    )

    to_city = db.Column(
        db.String(100),
        nullable=False
    )

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

    fare = db.Column(
        db.Integer,
        nullable=False
    )

    available_seats = db.Column(
        db.Integer,
        default=40
    )

    status = db.Column(
        db.String(20),
        default="Active"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    bus = db.relationship(
        "Bus",
        backref="trips"
    )

    def __repr__(self):
        return f"<Trip {self.from_city} -> {self.to_city}>"