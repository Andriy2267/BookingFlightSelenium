from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Flight(Base):
    __tablename__ = 'flights'

    id = Column(Integer, primary_key=True, autoincrement=True)
    carrier_name = Column(String)
    trip_duration = Column(String)
    shown_price = Column(String)
    total_price = Column(String)
    cabin_class = Column(String)
    flight_no = Column(String)
