from datetime import datetime
from . import db


class Bus(db.Model):
    __tablename__ = "buses"

    id = db.Column(db.Integer, primary_key=True)

    # Operator
    operator_id = db.Column(
        db.Integer,
        db.ForeignKey("operators.id"),
        nullable=False
    )

    # Bus Details
    bus_name = db.Column(
        db.String(100),
        nullable=False
    )

    bus_number = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )

    registration_number = db.Column(
        db.String(50)
    )

    bus_type = db.Column(
        db.String(30),
        default="AC Sleeper"
    )

    total_seats = db.Column(
        db.Integer,
        default=40
    )

    amenities = db.Column(
        db.Text
    )

    # Bus Photos
    front_photo = db.Column(db.String(255))
    back_photo = db.Column(db.String(255))
    left_photo = db.Column(db.String(255))
    right_photo = db.Column(db.String(255))

    # Approval Status
    status = db.Column(
        db.String(20),
        default="Pending"
    )

    # Created Time
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Relationship
    operator = db.relationship(
        "Operator",
        backref="buses"
    )

    def __repr__(self):
        return f"<Bus {self.bus_name}>"