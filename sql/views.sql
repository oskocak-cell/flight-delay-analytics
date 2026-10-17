-- No ranking is implied by a view: apply ORDER BY when selecting results.
CREATE VIEW delay_by_departure_airport AS
SELECT a.airport_id, a.airport_name, a.city, COUNT(*) AS total_flights,
       AVG(f.departure_delay_min) AS avg_departure_delay_min,
       AVG(f.arrival_delay_min) AS avg_arrival_delay_min
FROM fact_flight f JOIN dim_airport a ON f.departure_airport_key = a.airport_key
GROUP BY a.airport_id, a.airport_name, a.city;

CREATE VIEW delay_by_airline AS
SELECT a.owner_company AS airline, COUNT(*) AS total_flights,
       AVG(f.departure_delay_min) AS avg_departure_delay_min,
       AVG(f.arrival_delay_min) AS avg_arrival_delay_min,
       SUM(f.is_delayed) AS delayed_flights
FROM fact_flight f JOIN dim_aircraft a ON f.aircraft_key = a.aircraft_key
GROUP BY a.owner_company;

CREATE VIEW daily_operations AS
SELECT d.full_date, COUNT(*) AS total_flights,
       AVG(f.departure_delay_min) AS avg_departure_delay_min,
       AVG(f.arrival_delay_min) AS avg_arrival_delay_min,
       SUM(f.is_delayed) AS delayed_flights
FROM fact_flight f JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.full_date;
