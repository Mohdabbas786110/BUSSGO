from datetime import datetime
from . import db


class Operator(db.Model):
    __tablename__ = "operators"

    id = db.Column(db.Integer, primary_key=True)

    company_name = db.Column(db.String(150), nullable=False)

    owner_name = db.Column(db.String(100), nullable=False)

    mobile = db.Column(db.String(10), unique=True, nullable=False)

    address = db.Column(db.Text)

    status = db.Column(
    db.String(20),
    default="Pending"
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
        return f"<Operator {self.company_name}>"