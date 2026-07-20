from datetime import datetime
from . import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(100), nullable=False)

    mobile = db.Column(db.String(10), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True)

    password = db.Column(db.String(255))

    role = db.Column(
        db.String(20),
        default="passenger"
    )

    is_verified = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<User {self.full_name}>"