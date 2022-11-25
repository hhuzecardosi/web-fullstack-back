import unittest
from scripts.daily_update import get_daily_update, daily_update


class DailyUpdateTest(unittest.TestCase):
    def test_daily_update(self):
        dates = ['2022-11-19', '2022-11-20', '2022-11-21', '2022-11-22', '2022-11-23']
        # d1 = daily_update(dates[0])
        # d2 = daily_update(dates[1])
        # d3 = daily_update(dates[2])
        # d4 = daily_update(dates[3])
        d5 = daily_update(dates[4])
        # self.assertEqual(d1, True)
        # self.assertEqual(d2, True)
        # self.assertEqual(d3, True)
        # self.assertEqual(d4, True)
        self.assertEqual(d5, True)


if __name__ == '__main__':
    unittest.main()
