from flask import Flask, render_template, request
from flask_migrate import Migrate
from config import Config
from models import db, Trip
from routes.operator import operator

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)