-- Extracted from the original Pentaho report; execute with dw_airline selected.
SELECT
    da.airport_name,
    da.city,
    ROUND(AVG(ff.departure_delay_min), 2) AS avg_departure_delay_min,
    ROUND(AVG(ff.arrival_delay_min), 2)   AS avg_arrival_delay_min,
    COUNT(*) AS flight_count
FROM fact_flight ff
JOIN dim_airport da
    ON ff.departure_airport_key = da.airport_key
WHERE
    da.country IN ('USA', 'US', 'United States', 'United States of America')
    AND ff.departure_delay_min IS NOT NULL
    AND ff.arrival_delay_min IS NOT NULL
GROUP BY
    da.airport_id, da.airport_name, da.city, da.country
ORDER BY
    avg_departure_delay_min DESC,
    avg_arrival_delay_min DESC;
