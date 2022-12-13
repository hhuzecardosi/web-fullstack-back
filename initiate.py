from scripts.initiate_nba_database import populate_teams_collection, populate_players_collection, \
    populate_games_collection, populate_stats


print('STARTS INITIALIZATION OF DATABASE')
print('\t GETTING ALL NBA TEAMS')
populate_teams_collection()

print('\t GETTING ALL NBA PLAYERS')
populate_players_collection()

print('\t GETTING ALL NBA GAMES')
populate_games_collection()

print('\t POPULATING PLAYERS STATS FROM ALL PASSED GAMES')
populate_stats()

print('INITIALIZATION DONE')
