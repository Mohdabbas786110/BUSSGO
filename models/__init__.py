from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User

from .operator import Operator

from .bus import Bus

from .trip import Trip

from .booking import Booking

from .seat import Seat