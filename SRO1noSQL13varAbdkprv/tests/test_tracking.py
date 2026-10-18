import unittest
from datetime import datetime, timezone
from SRO1noSQL13varAbdkprv.src.queries import GPSHarness

class TestGPSTracking(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = GPSHarness()
        cls.v_id = "TEST-UNIT"
        cls.date = "2026-10-18"
        cls.ts = datetime.now(timezone.utc)
        cls.db.insert_point(cls.v_id, cls.date, cls.ts, 51.0, 71.0, 75.0, 300.0, "TEST")

    @classmethod
    def tearDownClass(cls):
        cls.db.delete_daily_track(cls.v_id, cls.date)
        cls.db.close()

    def test_get_latest_position(self):
        res = self.db.get_latest_position(self.v_id, self.date)
        self.assertIsNotNone(res)
        self.assertEqual(res.speed, 75.0)

    def test_speed_filtering(self):
        events = self.db.get_speeding_events(self.v_id, self.date, min_speed=50.0)
        self.assertGreaterEqual(len(events), 1)

if __name__ == '__main__':
    unittest.main()