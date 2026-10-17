"""Regression checks for clock rollover, grain, joins, and reproducibility."""
import csv
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_warehouse import build_database, signed_delay, flight_measures, export_reports

class DelayTests(unittest.TestCase):
    def test_midnight_late(self):
        self.assertEqual(signed_delay("00:10:00", "23:55:00"), 15)
    def test_midnight_early(self):
        self.assertEqual(signed_delay("23:55:00", "00:10:00"), -15)
    def test_normal_and_boundary(self):
        self.assertEqual(signed_delay("10:45:00", "10:00:00"), 45)
        self.assertEqual(signed_delay("10:00:00", "10:00:00"), 0)
    def test_overnight_duration(self):
        s={"scheduled_departure_time":"23:50:00", "scheduled_arrival_time":"01:50:00"}
        a={"actual_departure_time":"00:10:00", "actual_arrival_time":"02:00:00"}
        self.assertEqual(flight_measures(s,a), (120,110,20,10,1))
    def test_delay_threshold(self):
        s={"scheduled_departure_time":"10:00:00", "scheduled_arrival_time":"12:00:00"}
        for arrival, delayed in [("12:15:00",0),("12:16:00",1)]:
            a={"actual_departure_time":"10:15:00", "actual_arrival_time":arrival}
            self.assertEqual(flight_measures(s,a)[-1],delayed)
    def test_invalid_time_rejected(self):
        with self.assertRaises(ValueError): signed_delay("24:00:00","12:00:00")

class WarehouseTests(unittest.TestCase):
    def setUp(self):
        self.conn=sqlite3.connect(":memory:")
        build_database(self.conn,ROOT/"data/sample")
    def tearDown(self): self.conn.close()
    def test_grain_and_foreign_keys(self):
        self.assertEqual(self.conn.execute("SELECT COUNT(*), COUNT(DISTINCT actual_flight_id) FROM fact_flight").fetchone()[:],(250,250))
        self.assertEqual(self.conn.execute("PRAGMA foreign_key_check").fetchall(),[])
    def test_midnight_corrections_and_duration_identity(self):
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM fact_flight WHERE arrival_delay_min < -720 OR arrival_delay_min >= 720").fetchone()[0],0)
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM fact_flight WHERE actual_duration_min != scheduled_duration_min + arrival_delay_min - departure_delay_min").fetchone()[0],0)
    def test_rollups_preserve_counts(self):
        for view in ["delay_by_departure_airport","delay_by_airline","daily_operations"]:
            self.assertEqual(self.conn.execute(f"SELECT SUM(total_flights) FROM {view}").fetchone()[0],250)
    def test_current_sample_results(self):
        row=self.conn.execute("SELECT AVG(departure_delay_min),AVG(arrival_delay_min),SUM(is_delayed) FROM fact_flight").fetchone()
        self.assertAlmostEqual(row[0],14.28);self.assertAlmostEqual(row[1],18.856);self.assertEqual(row[2],196)
    def test_exports_are_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);export_reports(self.conn,p)
            first={f.name:f.read_bytes() for f in p.iterdir()};export_reports(self.conn,p)
            self.assertEqual(first,{f.name:f.read_bytes() for f in p.iterdir()})

if __name__ == "__main__": unittest.main()
