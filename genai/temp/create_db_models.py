# using resolved_model self.resolved_model FIXME
# created from response, to create create_db_models.sqlite, with test data
#    that is used to create project
# should run without error in manager 
#    if not, check for decimal, indent, or import issues

import decimal
import logging
import sqlalchemy
from sqlalchemy.sql import func 
from logic_bank.logic_bank import Rule
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, Numeric, Boolean, Text, DECIMAL
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from datetime import date   
from datetime import datetime
from typing import List


logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

Base = declarative_base()  # from system/genai/create_db_models_inserts/create_db_models_prefix.py


from sqlalchemy.dialects.sqlite import *

class Aircraft(Base):
    """description: Represents aircraft used in flights, including attributes such as model, manufacturer, seats, and includes baggage weight and passenger count as derived attributes."""
    __tablename__ = 'aircraft'
    id = Column(Integer, primary_key=True, autoincrement=True)
    model = Column(String(50), nullable=True)
    manufacturer = Column(String(100), nullable=True)
    seats = Column(Integer, nullable=True)
    airline_id = Column(Integer, ForeignKey('airline.id'), nullable=True)
    baggage_weight_total = Column(Float, nullable=True)
    passenger_count = Column(Integer, nullable=True)
    maintenance_count = Column(Integer, nullable=True)
    allowable_uses = Column(Integer, nullable=True)

class Passenger(Base):
    """description: Contains passenger details for a flight, including name and seat number, with lounge_access_count as a derived attribute."""
    __tablename__ = 'passenger'
    id = Column(Integer, primary_key=True, autoincrement=True)
    flight_id = Column(Integer, ForeignKey('flight.id'))
    name = Column(String(100), nullable=True)
    seat_number = Column(String(10), nullable=True)
    lounge_access_count = Column(Integer, nullable=True)

class FlightCrew(Base):
    """description: Junction table to map crew members to flights with positions, role_count as a derived attribute."""
    __tablename__ = 'flight_crew'
    id = Column(Integer, primary_key=True, autoincrement=True)
    flight_id = Column(Integer, ForeignKey('flight.id'))
    crew_member_id = Column(Integer, ForeignKey('crew_member.id'))
    position = Column(String(30), nullable=True)
    role_count = Column(Integer, nullable=True)

class MaintenanceRecord(Base):
    """description: Maintenance logs for aircraft, detailing the maintenance performed, as well as maintaining count for maintenance frequency."""
    __tablename__ = 'maintenance_record'
    id = Column(Integer, primary_key=True, autoincrement=True)
    aircraft_id = Column(Integer, ForeignKey('aircraft.id'))
    maintenance_date = Column(Date, nullable=True)
    description = Column(String(200), nullable=True)


# end of model classes


try:
    
    
    # ALS/GenAI: Create an SQLite database
    import os
    mgr_db_loc = True
    if mgr_db_loc:
        print(f'creating in manager: sqlite:///system/genai/temp/create_db_models.sqlite')
        engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
    else:
        current_file_path = os.path.dirname(__file__)
        print(f'creating at current_file_path: {current_file_path}')
        engine = create_engine(f'sqlite:///{current_file_path}/create_db_models.sqlite')
    Base.metadata.create_all(engine)
    
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # ALS/GenAI: Prepare for sample data
    
    
    session.commit()
    aircraft1 = Aircraft(model="Boeing 737", manufacturer="Boeing", seats=160, airline_id=1, baggage_weight_total=0.0, passenger_count=0, maintenance_count=0) # Ensure these derived attributes are manually set for test data
    aircraft2 = Aircraft(model="Airbus A380", manufacturer="Airbus", seats=500, airline_id=2, baggage_weight_total=0.0, passenger_count=0, maintenance_count=0)
    aircraft3 = Aircraft(model="Boeing 787", manufacturer="Boeing", seats=300, airline_id=3, baggage_weight_total=0.0, passenger_count=0, maintenance_count=0)
    aircraft4 = Aircraft(model="Airbus A350", manufacturer="Airbus", seats=350, airline_id=4, baggage_weight_total=0.0, passenger_count=0, maintenance_count=0)
    passenger1 = Passenger(flight_id=1, name="Michael Johnson", seat_number="12A", lounge_access_count=0) # Initialize lounge_access_count based on access availability
    passenger2 = Passenger(flight_id=2, name="Linda Bennett", seat_number="14B", lounge_access_count=0)
    passenger3 = Passenger(flight_id=3, name="Paul Green", seat_number="8C", lounge_access_count=0)
    passenger4 = Passenger(flight_id=4, name="Laura Blue", seat_number="2D", lounge_access_count=0)
    flight_crew1 = FlightCrew(flight_id=1, crew_member_id=1, position="Pilot", role_count=0) # Ensure role_count is initialized correctly
    flight_crew2 = FlightCrew(flight_id=1, crew_member_id=2, position="Co-Pilot", role_count=0)
    flight_crew3 = FlightCrew(flight_id=2, crew_member_id=3, position="Flight Attendant", role_count=0)
    flight_crew4 = FlightCrew(flight_id=3, crew_member_id=4, position="Pilot", role_count=0)
    maintenance_record1 = MaintenanceRecord(aircraft_id=1, maintenance_date=date(2023, 9, 1), description="Engine Check") # Maintain accurate count management
    maintenance_record2 = MaintenanceRecord(aircraft_id=2, maintenance_date=date(2023, 8, 25), description="Landing Gear Replacement")
    maintenance_record3 = MaintenanceRecord(aircraft_id=3, maintenance_date=date(2023, 7, 15), description="Fuel System Inspection")
    maintenance_record4 = MaintenanceRecord(aircraft_id=4, maintenance_date=date(2023, 10, 2), description="Cabin Pressure Check")
    
    
    
    session.add_all([aircraft1, aircraft2, aircraft3, aircraft4, passenger1, passenger2, passenger3, passenger4, flight_crew1, flight_crew2, flight_crew3, flight_crew4, maintenance_record1, maintenance_record2, maintenance_record3, maintenance_record4])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
