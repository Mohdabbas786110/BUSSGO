from app import app
from models import db, Bus, Trip
from datetime import date, time


routes = [
    ("Lucknow", "Ayodhya", "Abbas Express", "BUSGO101", "AC Seater", 350, time(7, 0), time(9, 30)),
    ("Lucknow", "Ayodhya", "Abbas Travels Premium", "BUSGO102", "AC Sleeper", 450, time(10, 0), time(12, 30)),

    ("Ayodhya", "Lucknow", "Abbas Express", "BUSGO101", "AC Seater", 350, time(14, 0), time(16, 30)),
    ("Ayodhya", "Lucknow", "Abbas Travels Premium", "BUSGO102", "AC Sleeper", 450, time(18, 0), time(20, 30)),

    ("Lucknow", "Gorakhpur", "Abbas Superfast", "BUSGO103", "AC Seater", 650, time(6, 0), time(11, 0)),
    ("Lucknow", "Gorakhpur", "Abbas Royal", "BUSGO104", "AC Sleeper", 850, time(21, 0), time(4, 0)),

    ("Gorakhpur", "Lucknow", "Abbas Superfast", "BUSGO103", "AC Seater", 650, time(12, 0), time(17, 0)),
    ("Gorakhpur", "Lucknow", "Abbas Royal", "BUSGO104", "AC Sleeper", 850, time(22, 0), time(5, 0)),

    ("Basti", "Lucknow", "Abbas Superfast", "BUSGO103", "AC Seater", 500, time(8, 0), time(12, 0)),
    ("Basti", "Lucknow", "Abbas Royal", "BUSGO104", "AC Sleeper", 650, time(20, 0), time(0, 0)),

    ("Lucknow", "Basti", "Abbas Superfast", "BUSGO103", "AC Seater", 500, time(13, 0), time(17, 0)),
    ("Lucknow", "Basti", "Abbas Royal", "BUSGO104", "AC Sleeper", 650, time(22, 0), time(2, 0)),

    ("Lucknow", "Kanpur", "Abbas Express", "BUSGO101", "AC Seater", 250, time(8, 0), time(10, 0)),
    ("Lucknow", "Kanpur", "Abbas Travels Premium", "BUSGO102", "AC Sleeper", 350, time(18, 0), time(20, 0)),

    ("Kanpur", "Lucknow", "Abbas Express", "BUSGO101", "AC Seater", 250, time(11, 0), time(13, 0)),
    ("Kanpur", "Lucknow", "Abbas Travels Premium", "BUSGO102", "AC Sleeper", 350, time(21, 0), time(23, 0)),
]


with app.app_context():

    OPERATOR_ID = 2
    JOURNEY_DATE = date(2026, 10, 5)

    for (
        from_city,
        to_city,
        bus_name,
        bus_number,
        bus_type,
        fare,
        departure,
        arrival
    ) in routes:

        # Find or create bus
        bus = Bus.query.filter_by(
            bus_number=bus_number
        ).first()

        if not bus:
            bus = Bus(
                operator_id=OPERATOR_ID,
                bus_name=bus_name,
                bus_number=bus_number,
                registration_number=bus_number,
                bus_type=bus_type,
                total_seats=40,
                amenities="AC, Charging Point, Water Bottle",
                status="Approved"
            )

            db.session.add(bus)
            db.session.commit()

            print("BUS CREATED:", bus_name)

        # Check duplicate trip
        existing_trip = Trip.query.filter_by(
            bus_id=bus.id,
            from_city=from_city,
            to_city=to_city,
            departure_time=departure
        ).first()

        if not existing_trip:

            trip = Trip(
                bus_id=bus.id,
                from_city=from_city,
                to_city=to_city,
                boarding_point=from_city + " Bus Stand",
                dropping_point=to_city + " Bus Stand",
                journey_date=JOURNEY_DATE,
                departure_time=departure,
                arrival_time=arrival,
                fare=fare,
                total_seats=40,
                available_seats=40,
                status="Scheduled"
            )

            db.session.add(trip)

            print(
                "TRIP CREATED:",
                from_city,
                "->",
                to_city
            )

    db.session.commit()

    print("\n================================")
    print("ALL ROUTES ADDED SUCCESSFULLY")
    print("================================")