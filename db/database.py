from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Flight, Base

DB_URL = "postgresql://postgres:Chopek696@localhost:5432/BookingFlight"

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)


def create_tables():
    Base.metadata.create_all(engine)


def save_flight_to_db(data: list):
    session = Session()
    try:
        flight = Flight(
            carrier_name=data[0],
            trip_duration=data[1],
            shown_price=data[2],
            total_price=data[3],
            cabin_class=data[4],
            flight_no=data[5],
        )
        session.add(flight)
        session.commit()

    except Exception as e:
        session.rollback()
        print("DB Error:", e)
        
    finally:
        session.close()
