from datetime import datetime
from . import db


class Seat(db.Model):
    __tablename__ = "seats"

    id = db.Column(db.Integer, primary_key=True)

    trip_id = db.Column(
        db.Integer,
        db.ForeignKey("trips.id"),
        nullable=False
    )

    seat_number = db.Column(
        db.String(10),
        nullable=False
    )

    seat_type = db.Column(
        db.String(20),
        default="Seater"
    )

    is_booked = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    trip = db.relationship(
        "Trip",
        backref="seats"
    )

    def __repr__(self):
        return f"<Seat {self.seat_number}>"