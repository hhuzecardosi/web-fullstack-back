from datetime import datetime, timedelta
from bson import ObjectId
from pydash.objects import get

from database.database_connection import database_connection


def get_player(player_id):
    try:
        player_collection = database_connection()['players']
        player = player_collection.find_one({'_id': ObjectId(player_id)})
        if not player:
            return {'context': 'player', 'method': 'get_player', 'error': 'PLAYER_NOT_FOUND', 'code': 404}
        return {'context': 'player', 'method': 'get_player', 'data': player, 'code': 200}
    except Exception as e:
        print(e)
        return {'context': 'player', 'method': 'get_player', 'error': str(e), 'code': 500}


def get_night_stats():
    try:
        player_collection = database_connection()['players']
        players = list(player_collection.find())
        if len(players) == 0:
            return {'context': 'player', 'method': 'get_player', 'error': 'PLAYER_NOT_FOUND', 'code': 404}
        night_players = []
        for p in players:
            date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
            date = datetime.strptime(date, '%Y-%m-%d')
            statistics = [stats for i, stats in enumerate(get(p, 'stats')) if stats['date'] == date]
            if len(statistics) > 0:
                night_players.append({'_id': p['_id'], 'name': p['name'], 'stats': statistics})
        return {'context': 'player', 'method': 'get_player', 'data': night_players, 'code': 200}
    except Exception as e:
        return {'context': 'player', 'method': 'get_player', 'error': str(e), 'code': 500}
