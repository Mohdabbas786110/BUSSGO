from datetime import datetime
from . import db


class Bus(db.Model):
    __tablename__ = "buses"

    id = db.Column(db.Integer, primary_key=True)

    operator_id = db.Column(
        db.Integer,
        db.ForeignKey("operators.id"),
        nullable=False
    )

    bus_name = db.Column(db.String(100), nullable=False)

    bus_number = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )

    bus_type = db.Column(
        db.String(30),
        default="AC Sleeper"
    )

    total_seats = db.Column(
        db.Integer,
        default=40
    )

    amenities = db.Column(db.Text)

    status = db.Column(
        db.String(20),
        default="Active"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    operator = db.relationship(
        "Operator",
        backref="buses"
    )

    def __repr__(self):
        return f"<Bus {self.bus_name}>"