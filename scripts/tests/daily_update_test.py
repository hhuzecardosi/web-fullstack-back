import unittest
from datetime import datetime, timedelta
from scripts.daily_update import get_daily_update, daily_update


class DailyUpdateTest(unittest.TestCase):
    def test_daily_update(self):
        date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        stats = daily_update(date)
        self.assertEqual(stats, True)


if __name__ == '__main__':
    unittest.main()
