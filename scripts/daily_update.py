from nba_api.live.nba.endpoints import boxscore
from nba_api.live.nba.endpoints import scoreboard
from pydash import get
from database import database_connection
from common.utils import difference_in_dates, compute_player_stats


def get_daily_update():
    try:
        client = database_connection.database_connection()
        player_collection = client['players']
        game_collection = client['games']
        games = scoreboard.ScoreBoard().get_dict()
        for game in get(games, 'scoreboard.games', []):
            game_id = get(game, 'gameId', '')
            db_game = game_collection.find_one({'external_id': game_id})
            if db_game:
                if db_game['status'] != 'FINAL':
                    players = boxscore.BoxScore(game_id).get_dict()
                    # home team players
                    for player in get(players, 'game.homeTeam.players', []):
                        compute_player_stats(player_collection, db_game, player)
                    # away team players
                    for player in get(players, 'game.awayTeam.players', []):
                        compute_player_stats(player_collection, db_game, player)
                    db_game['status'] = 'FINAL'
                    db_game['h_score'] = game['homeTeam']['score']
                    db_game['v_score'] = game['awayTeam']['score']
                    print(db_game)
                    game_collection.update_one({'_id': db_game['_id']}, {'$set': db_game})
                    print('Game Done')
        print('DONE')
        return True
    except Exception as e:
        print(e)
        return False
