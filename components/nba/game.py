from datetime import datetime, timedelta

from database.database_connection import database_connection


def get_games_by_date(string_date):
    try:
        game_collection = database_connection()['games']
        date = datetime.strptime(string_date, '%Y-%m-%d')
        games = list(game_collection.find({'date': date}))
        if len(games) == 0:
            return {'context': 'game', 'method': 'get_by_date', 'error': 'NO_GAME_FOUND', 'code': 404}
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
