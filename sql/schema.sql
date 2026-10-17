-- Portfolio reproduction, using SQLite. Four dimensions match the saved DW model.
PRAGMA foreign_keys = ON;
CREATE TABLE airports (airport_id INTEGER PRIMARY KEY, airport_name TEXT NOT NULL, city TEXT NOT NULL, country TEXT NOT NULL);
CREATE TABLE aircraft (aircraft_id INTEGER PRIMARY KEY, registration_number TEXT NOT NULL, model TEXT NOT NULL, capacity INTEGER NOT NULL CHECK(capacity>0), owner_company TEXT NOT NULL);
CREATE TABLE pilots (pilot_id INTEGER PRIMARY KEY);
CREATE TABLE flight_schedule (
 schedule_id INTEGER PRIMARY KEY,
 aircraft_aircraft_id INTEGER NOT NULL REFERENCES aircraft,
 airports_departure_airport_id INTEGER NOT NULL REFERENCES airports,
 airports_arrival_airport_id INTEGER NOT NULL REFERENCES airports,
 scheduled_date TEXT NOT NULL, scheduled_departure_time TEXT NOT NULL, scheduled_arrival_time TEXT NOT NULL);
CREATE TABLE actual_flights (
 actual_flight_id INTEGER PRIMARY KEY,
 flight_schedule_schedule_id INTEGER NOT NULL REFERENCES flight_schedule,
 pilots_pilot_id INTEGER NOT NULL REFERENCES pilots,
 actual_departure_time TEXT NOT NULL, actual_arrival_time TEXT NOT NULL);
CREATE TABLE dim_date (date_key INTEGER PRIMARY KEY, full_date TEXT UNIQUE NOT NULL, year INTEGER NOT NULL, month INTEGER NOT NULL, day INTEGER NOT NULL, day_of_week INTEGER NOT NULL);
CREATE TABLE dim_airport (airport_key INTEGER PRIMARY KEY, airport_id INTEGER UNIQUE NOT NULL, airport_name TEXT NOT NULL, city TEXT NOT NULL, country TEXT NOT NULL);
CREATE TABLE dim_aircraft (aircraft_key INTEGER PRIMARY KEY, aircraft_id INTEGER UNIQUE NOT NULL, registration_number TEXT NOT NULL, model TEXT NOT NULL, capacity INTEGER NOT NULL, owner_company TEXT NOT NULL);
CREATE TABLE dim_pilot (pilot_key INTEGER PRIMARY KEY, pilot_id INTEGER UNIQUE NOT NULL);
CREATE TABLE fact_flight (
 flight_key INTEGER PRIMARY KEY,
 actual_flight_id INTEGER UNIQUE NOT NULL,
 schedule_id INTEGER NOT NULL,
 date_key INTEGER NOT NULL REFERENCES dim_date,
 aircraft_key INTEGER NOT NULL REFERENCES dim_aircraft,
 departure_airport_key INTEGER NOT NULL REFERENCES dim_airport,
 arrival_airport_key INTEGER NOT NULL REFERENCES dim_airport,
 pilot_key INTEGER NOT NULL REFERENCES dim_pilot,
 scheduled_departure_time TEXT NOT NULL, scheduled_arrival_time TEXT NOT NULL,
 actual_departure_time TEXT NOT NULL, actual_arrival_time TEXT NOT NULL,
 scheduled_duration_min INTEGER NOT NULL CHECK(scheduled_duration_min>0),
 actual_duration_min INTEGER NOT NULL CHECK(actual_duration_min>0),
 departure_delay_min INTEGER NOT NULL, arrival_delay_min INTEGER NOT NULL,
 is_delayed INTEGER NOT NULL CHECK(is_delayed IN (0,1)));
