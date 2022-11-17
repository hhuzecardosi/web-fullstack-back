from datetime import datetime
from common.config_utils import get_file_from_path
from database import database_connection
from nba_api.stats.static import teams
from pydash.objects import get, set_
from nba_api.stats.endpoints import commonteamroster
from nba_api.live.nba.endpoints import boxscore
import time
from common.utils import difference_in_dates, compute_player_stats


def initiate_database():
    try:
        # Database connexion
        client = database_connection.database_connection()
        team_collection = client['teams']
        player_collection = client['players']
        game_collection = client['games']

        print('-- Create Team --')
        # create teams
        db_teams = list(team_collection.find())
        if len(db_teams) < 1:
            nba_teams = teams.get_teams()
            for team in nba_teams:
                db_team = {'external_id': get(team, 'id'), 'name': get(team, 'full_name'),
                           'code': get(team, 'abbreviation')}
                team_id = team_collection.find_one({'external_id': db_team['external_id']})
                if not team_id and db_team['external_id']:
                    team_collection.insert_one(db_team)

        print('-- Create Players --')
        # create player
        nba_teams = team_collection.find()
        players = list(player_collection.find())
        if len(players) < 500:
            players = []
            for team in nba_teams:
                external_id = get(team, 'external_id', '')
                if get(team, 'players') and len(get(team, 'players', [])) > 0:
                    print('Coucou', team['name'])
                    pass
                roster = commonteamroster.CommonTeamRoster(external_id).get_dict()['resultSets'][0]
                for player in roster['rowSet']:
                    db_player = {'external_id': player[14], 'name': player[3], 'number': player[6],
                                 'team': team['_id'], 'stats': []}
                    player_id = player_collection.find_one({'external_id': db_player['external_id']})
                    if not player_id and db_player['external_id']:
                        players.append(db_player)
                time.sleep(3)
            if len(players) > 0:
                player_collection.insert_many(players)

        print('-- Populate Players in teams --')
        for team in nba_teams:
            _id = team['_id']
            if not get(team, 'players'): set_(team, 'players', [])
            team_players = list(player_collection.find({'team': _id}))
            for player in team_players:
                if player['_id'] not in team['players']:
                    team['players'].append(player['_id'])
            team_collection.update_one({'_id': _id}, {'$set': team})

        print('-- Create Schedule --')
        schedule = get_file_from_path('config/nba_schedule.json')
        for game in schedule['games']:
            date = datetime.strptime(str(game['date']).split(' ')[0], '%m/%d/%Y')
            game['date'] = date
            if game['status'] == 3 or difference_in_dates(date, datetime.now()) < 0:
                # Match ended need to enter stats
                try:
                    g_boxscore = boxscore.BoxScore(game_id=game['external_id']).get_dict()
                    game['h_score'] = g_boxscore['game']['homeTeam']['score']
                    game['v_score'] = g_boxscore['game']['awayTeam']['score']
                    # stats for home team's players
                    h_players = g_boxscore['game']['homeTeam']['players']
                    for player in h_players:
                        compute_player_stats(player_collection, game, player)
                    # stats for away team's players
                    v_players = g_boxscore['game']['awayTeam']['players']
                    for player in v_players:
                        compute_player_stats(player_collection, game, player)
                except Exception as e:
                    print(e)
                game['status'] = 'FINAL'
            else:
                game['status'] = 'TO_BE'
            db_game = game_collection.find_one({'external_id': game['external_id']})
            if db_game:
                game['_id'] = db_game['_id']
                game_collection.update_one({'_id': db_game['_id']}, {'$set': game})
            else:
                game_collection.insert_one(game)
        print('DONE')
        return True
    except Exception as e:
        print(e)
        return False


def get_total_players():
    client = database_connection.database_connection()
    player_collection = client['players']
    return len(list(player_collection.find()))
