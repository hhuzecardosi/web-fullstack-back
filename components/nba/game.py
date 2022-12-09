from datetime import datetime, timedelta
from pydash.objects import set_, get

from .team import get_team
from common.utils import transform_games_to_export, create_deck
from database.database_connection import database_connection


def get_games_by_date(string_date):
    try:
        game_collection = database_connection()['games']
        date = datetime.strptime(string_date, '%Y-%m-%d')
        games = list(game_collection.find({'date': date}))
        if len(games) == 0:
            return {'context': 'game', 'method': 'get_by_date', 'error': 'NO_GAME_FOUND', 'code': 404}
        for game in games:
            h_team = get_team(get(game, 'h_team', ''))['data'] if get_team(get(game, 'h_team', ''))['code'] == 200 \
                else {'name': 'UNKNOWN', '_id': 'UNKNOWN'}
            v_team = get_team(get(game, 'v_team', ''))['data'] if get_team(get(game, 'v_team', ''))['code'] == 200 \
                else {'name': 'UNKNOWN', '_id': 'UNKNOWN'}
            set_(game, '_id', str(game['_id']))
            set_(game, 'h_team', {'name': get(h_team, 'name', ''), '_id': str(get(h_team, '_id', ''))})
            set_(game, 'v_team', {'name': get(v_team, 'name', ''), '_id': str(get(v_team, '_id', ''))})
            set_(game, 'date', game['date'].strftime('%Y-%m-%d'))
        return {'context': 'game', 'method': 'get_by_date', 'data': games, 'code': 200}
    except Exception as e:
        return {'context': 'game', 'method': 'get_by_date', 'error': str(e), 'code': 500}


def get_night_results():
    try:
        date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        result = get_games_by_date(date)
        if 'error' in result:
            return result
        return {'context': 'game', 'method': 'get_night_result', 'data': result['data'], 'code': 200}
    except Exception as e:
        return {'context': 'game', 'method': 'get_night_result', 'error': str(e), 'code': 500}


def get_games_of_the_week(string_date):
    try:
        first_day = create_deck(string_date)['from']
        last_day = create_deck(string_date)['to']
        delta = last_day - first_day
        dates = [first_day + timedelta(days=i) for i in range(delta.days + 1)]
        games = []
        for date in dates:
            data = {'date': date.strftime('%Y-%m-%d')}
            games_date = get_games_by_date(date.strftime('%Y-%m-%d'))
            if get(games_date, 'code', 500) == 200:
                set_(data, 'games', games_date['data'])
            else:
                return games_date
            games.append(data)
        return {'context': 'game', 'method': 'get_games_of_the_week', 'data': games, 'code': 200}
    except Exception as e:
        print(e)
        return {'context': 'game', 'method': 'get_games_of_the_week', 'error': str(e), 'code': 500}
