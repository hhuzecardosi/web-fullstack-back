import unittest
from scripts.daily_update import get_daily_update


class DailyUpdateTest(unittest.TestCase):
    def test_daily_update(self):
        test = get_daily_update()
        self.assertEqual(test, True)


if __name__ == '__main__':
    unittest.main()
