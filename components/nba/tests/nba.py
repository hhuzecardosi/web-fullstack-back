import unittest
from components.nba.game import get_games_by_date, get_night_results
from components.nba.player import get_night_stats


class GameTest(unittest.TestCase):
    def test_get_game_by_date(self):
        games = get_games_by_date('2022-11-17')
        print(games)
        self.assertEqual(True, True)  # add assertion here

    def test_night_result(self):
        games = get_night_results()
        print(games)
        self.assertEqual(True, True)


class PlayerTest(unittest.TestCase):
    def test_night_stats(self):
        players = get_night_stats()
        print(players)
        print(len(players['data']))
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
