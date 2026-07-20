from datetime import datetime
from . import db


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    trip_id = db.Column(
        db.Integer,
        db.ForeignKey("trips.id"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    passenger_name = db.Column(
        db.String(100),
        nullable=False
    )

    passenger_mobile = db.Column(
        db.String(10),
        nullable=False
    )

    seat_number = db.Column(
        db.String(10),
        nullable=False
    )

    fare = db.Column(
        db.Integer,
        nullable=False
    )

    payment_status = db.Column(
        db.String(20),
        default="Pending"
    )

    booking_status = db.Column(
        db.String(20),
        default="Booked"
    )

    booking_time = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    trip = db.relationship(
        "Trip",
        backref="bookings"
    )

    user = db.relationship(
        "User",
        backref="bookings"
    )

    def __repr__(self):
        return (
            f"<Booking {self.passenger_name} "
            f"{self.seat_number}>"
        )