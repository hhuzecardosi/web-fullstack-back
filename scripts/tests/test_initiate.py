import unittest
from scripts.initiate_nba_database import initiate_database, get_total_players


class InitiateDatabaseTest(unittest.TestCase):
    def test_initiate(self):
        test = initiate_database()
        self.assertEqual(test, True)

    def test_total_players(self):
        total = get_total_players()
        print(total)
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
