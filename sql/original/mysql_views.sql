

CREATE VIEW dw_airline.vw_flight_delay_by_airport AS
SELECT
  da.airport_name AS departure_airport,
  COUNT(*) AS total_flights,
  AVG(ff.departure_delay_min) AS avg_departure_delay_min
FROM dw_airline.fact_flight ff
JOIN dw_airline.dim_airport da
  ON ff.departure_airport_key = da.airport_key
WHERE ff.departure_delay_min IS NOT NULL
GROUP BY da.airport_name
ORDER BY avg_departure_delay_min DESC;


SELECT * FROM dw_airline.vw_flight_delay_by_airport;





CREATE VIEW dw_airline.vw_daily_operations_delay AS
SELECT
  dd.full_date,
  COUNT(*) AS flights_count,
  AVG(ff.departure_delay_min) AS avg_departure_delay_min,
  AVG(ff.arrival_delay_min) AS avg_arrival_delay_min
FROM dw_airline.fact_flight ff
JOIN dw_airline.dim_date dd
  ON ff.date_key = dd.date_key
WHERE ff.departure_delay_min IS NOT NULL
  AND ff.arrival_delay_min IS NOT NULL
GROUP BY dd.full_date
ORDER BY avg_arrival_delay_min DESC;


SELECT * FROM dw_airline.vw_daily_operations_delay;



CREATE VIEW dw_airline.vw_top_delayed_airlines_departure AS
SELECT
  da.owner_company AS airline,
  COUNT(*) AS flights_count,
  AVG(ff.departure_delay_min) AS avg_departure_delay_min
FROM dw_airline.fact_flight ff
JOIN dw_airline.dim_aircraft da
  ON ff.aircraft_key = da.aircraft_key
WHERE ff.departure_delay_min IS NOT NULL
GROUP BY da.owner_company
ORDER BY avg_departure_delay_min DESC;

SELECT * FROM dw_airline.vw_top_delayed_airlines_departure;





CREATE VIEW dw_airline.vw_top_delayed_airlines_arrival AS
SELECT
  da.owner_company AS airline,
  COUNT(*) AS flights_count,
  AVG(ff.arrival_delay_min) AS avg_arrival_delay_min
FROM dw_airline.fact_flight ff
JOIN dw_airline.dim_aircraft da
  ON ff.aircraft_key = da.aircraft_key
WHERE ff.arrival_delay_min IS NOT NULL
GROUP BY da.owner_company
ORDER BY avg_arrival_delay_min DESC;

SELECT * FROM dw_airline.vw_top_delayed_airlines_arrival;
