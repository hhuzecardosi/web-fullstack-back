from bson import ObjectId
from pydash.objects import get, set_

from database.database_connection import database_connection


def get_team(team_id):
    try:
        team_collection = database_connection()['teams']
        player_collection = database_connection()['players']
        team = team_collection.find_one({'_id': ObjectId(team_id)})
        if not team:
            return {'context': 'team', 'method': 'get_team', 'error': 'TEAM_NOT_FOUND', 'code': 404}
        players = []
        for player_id in get(team, 'players', []):
            player = player_collection.find_one({'_id': player_id})
            if player:
                players.append({'_id': get(player, '_id'), 'name': get(player, 'name')})
        set_(team, 'players', players)
        return {'context': 'team', 'method': 'get_team', 'data': team, 'code': 200}
    except Exception as e:
        return {'context': 'team', 'method': 'get_team', 'error': str(e), 'code': 500}
