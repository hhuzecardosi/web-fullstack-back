from nba_api.live.nba.endpoints import boxscore
from nba_api.live.nba.endpoints import scoreboard
from pydash import get


def get_daily_update():
    try:
        games = scoreboard.ScoreBoard().get_dict()
        for game in get(games, 'scoreboard.games', []):
            game_id = get(game, 'gameId', '')
            players = boxscore.BoxScore(game_id).get_dict()
            # home team players
            print('Home Team', players['game']['homeTeam']['teamTricode'])
            for player in get(players, 'game.homeTeam.players', []):
                print('\t{0} - {1}'.format(player['name'], player['status']))
            # away team players
            print('Away Team', players['game']['awayTeam']['teamTricode'])
            for player in get(players, 'game.awayTeam.players', []):
                print('\t {0} - {1}'.format(player['name'], player['status']))
        return True
    except Exception as e:
        print(e)
        return False
