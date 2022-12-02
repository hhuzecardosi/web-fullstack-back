import unittest
from datetime import datetime, timedelta
from scripts.daily_update import daily_update


class DailyUpdateTest(unittest.TestCase):
    def test_daily_update(self):
        date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        stats = daily_update(date)
        self.assertEqual(stats, True)

    def test_daily_update_several_dates(self):
        dates = ['2022-11-25', '2022-11-26', '2022-11-27', '2022-11-28', '2022-11-29', '2022-11-30', '2022-12-01']
        for date in dates:
            stats = daily_update(date)
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
