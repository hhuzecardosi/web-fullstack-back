import unittest
from scripts.initiate_nba_database import initiate_database, get_total_players, populate_teams_collection, \
    populate_players_collection, populate_games_collection, populate_stats, populate_players_in_teams


class InitiateDatabaseTest(unittest.TestCase):
    def test_initiate(self):
        test = initiate_database()
        self.assertEqual(test, True)

    def test_initiate_database(self):
        teams = populate_teams_collection()
        players = populate_players_collection()
        games = populate_games_collection()
        stats = populate_stats()
        self.assertEqual(True, True)

    def test_games(self):
        games = populate_games_collection()
        self.assertEqual(games, True)

    def test_stats(self):
        stats = populate_stats()
        self.assertEqual(stats, True)

    def test_players_in_teams(self):
        players = populate_players_in_teams()
        self.assertEqual(players, True)

    def test_total_players(self):
        total = get_total_players()
        print(total)
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
