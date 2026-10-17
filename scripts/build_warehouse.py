"""Reproduce the course warehouse from minimized sample CSVs, using stdlib only.

This script is a new portfolio reproduction, not the original Pentaho workflow.
"""
import argparse
import csv
from datetime import date
import json
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
TABLES = ("airports", "aircraft", "pilots", "flight_schedule", "actual_flights")

def clock_minutes(value):
    """Parse an HH:MM:SS clock value, validating its range."""
    hour, minute, second = map(int, value.split(":"))
    if not (0 <= hour < 24 and 0 <= minute < 60 and second == 0):
        raise ValueError(f"Expected whole-minute clock time: {value}")
    return hour * 60 + minute

def signed_delay(actual, scheduled):
    """Closest signed clock difference, assuming delay is in [-12h, +12h)."""
    return (clock_minutes(actual) - clock_minutes(scheduled) + 720) % 1440 - 720

def flight_measures(schedule, actual):
    """Infer rollover consistently; source has no arrival dates or time zones."""
    dep = signed_delay(actual["actual_departure_time"], schedule["scheduled_departure_time"])
    arr = signed_delay(actual["actual_arrival_time"], schedule["scheduled_arrival_time"])
    duration = (clock_minutes(schedule["scheduled_arrival_time"]) - clock_minutes(schedule["scheduled_departure_time"])) % 1440
    actual_duration = duration + arr - dep
    if duration <= 0 or actual_duration <= 0:
        raise ValueError("Flight has a non-positive inferred duration")
    return duration, actual_duration, dep, arr, int(dep > 15 or arr > 15)

def load_source(conn, directory):
    for table in TABLES:
        with (directory / f"{table}.csv").open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            expected = [row[1] for row in conn.execute(f"PRAGMA table_info({table})")]
            if reader.fieldnames != expected:
                raise ValueError(f"Unexpected columns in {table}.csv")
            rows = list(reader)
        columns = ",".join(expected)
        marks = ",".join("?" for _ in expected)
        conn.executemany(f"INSERT INTO {table} ({columns}) VALUES ({marks})", [tuple(r[k] for k in expected) for r in rows])

def populate_dimensions(conn):
    for table, columns in [("airport", "airport_id, airport_name, city, country"), ("aircraft", "aircraft_id, registration_number, model, capacity, owner_company"), ("pilot", "pilot_id")]:
        source = {"airport": "airports", "aircraft": "aircraft", "pilot": "pilots"}[table]
        for key, row in enumerate(conn.execute(f"SELECT {columns} FROM {source} ORDER BY {table}_id").fetchall(), 1):
            marks = ",".join("?" for _ in range(len(row) + 1))
            conn.execute(f"INSERT INTO dim_{table} VALUES ({marks})", (key, *row))
    for row in conn.execute("SELECT DISTINCT scheduled_date FROM flight_schedule ORDER BY scheduled_date").fetchall():
        value = date.fromisoformat(row[0])
        conn.execute("INSERT INTO dim_date VALUES (?,?,?,?,?,?)", (int(value.strftime("%Y%m%d")), value.isoformat(), value.year, value.month, value.day, value.isoweekday()))

def populate_facts(conn):
    maps = {}
    for kind in ("airport", "aircraft", "pilot"):
        maps[kind] = dict(conn.execute(f"SELECT {kind}_id,{kind}_key FROM dim_{kind}"))
    schedules = {r["schedule_id"]: dict(r) for r in conn.execute("SELECT * FROM flight_schedule")}
    for key, actual in enumerate(conn.execute("SELECT * FROM actual_flights ORDER BY actual_flight_id").fetchall(), 1):
        schedule = schedules[actual["flight_schedule_schedule_id"]]
        values = (key, actual["actual_flight_id"], schedule["schedule_id"], int(schedule["scheduled_date"].replace("-", "")), maps["aircraft"][schedule["aircraft_aircraft_id"]], maps["airport"][schedule["airports_departure_airport_id"]], maps["airport"][schedule["airports_arrival_airport_id"]], maps["pilot"][actual["pilots_pilot_id"]], schedule["scheduled_departure_time"], schedule["scheduled_arrival_time"], actual["actual_departure_time"], actual["actual_arrival_time"], *flight_measures(schedule, actual))
        conn.execute("INSERT INTO fact_flight VALUES (" + ",".join("?" for _ in values) + ")", values)

def build_database(conn, source):
    conn.row_factory = sqlite3.Row
    conn.executescript((ROOT / "sql/schema.sql").read_text())
    load_source(conn, source)
    populate_dimensions(conn)
    populate_facts(conn)
    conn.executescript((ROOT / "sql/views.sql").read_text())
    if conn.execute("PRAGMA foreign_key_check").fetchall():
        raise ValueError("Foreign key validation failed")
    if conn.execute("SELECT COUNT(*) FROM fact_flight").fetchone()[0] != conn.execute("SELECT COUNT(*) FROM actual_flights").fetchone()[0]:
        raise ValueError("Fact grain does not match source executions")
    conn.commit()

def export_reports(conn, destination):
    destination.mkdir(parents=True, exist_ok=True)
    queries = {
        "delay_by_airport": "SELECT * FROM delay_by_departure_airport ORDER BY avg_departure_delay_min DESC,airport_id",
        "delay_by_airline": "SELECT * FROM delay_by_airline ORDER BY avg_departure_delay_min DESC,airline",
        "daily_operations": "SELECT * FROM daily_operations ORDER BY full_date",
    }
    for name, query in queries.items():
        cursor = conn.execute(query)
        with (destination / f"{name}.csv").open("w", newline="") as handle:
            writer = csv.writer(handle); writer.writerow([c[0] for c in cursor.description]); writer.writerows(cursor)
    summary = dict(conn.execute("SELECT COUNT(*) AS flights, AVG(departure_delay_min) AS avg_departure_delay_min, AVG(arrival_delay_min) AS avg_arrival_delay_min, SUM(is_delayed) AS delayed_flights FROM fact_flight").fetchone())
    summary["date_range"] = list(conn.execute("SELECT MIN(full_date), MAX(full_date) FROM dim_date").fetchone())
    summary["delay_definition"] = "departure > 15 minutes OR arrival > 15 minutes"
    (destination / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / "data/sample")
    parser.add_argument("--database", type=Path, default=ROOT / "build/flights.sqlite")
    parser.add_argument("--reports", type=Path, default=ROOT / "reports/reproduced")
    args = parser.parse_args()
    args.database.parent.mkdir(parents=True, exist_ok=True)
    if args.database.exists():
        parser.error("Database already exists; choose a new --database path to rebuild.")
    try:
        with sqlite3.connect(args.database) as conn:
            build_database(conn, args.source)
            print(json.dumps(export_reports(conn, args.reports), indent=2))
    except Exception:
        args.database.unlink(missing_ok=True)
        raise

if __name__ == "__main__":
    main()
