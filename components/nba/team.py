from bson import ObjectId
from pydash.objects import get, set_

from database.database_connection import database_connection


def get_team_with_player(team_id):
    try:
        player_collection = database_connection()['players']
        team_db = get_team(team_id)

        if team_db['code'] != 200:
            return team_db

        team = get(team_db, 'data', {})

        players = []
        for player_id in get(team, 'players', []):
            player = player_collection.find_one({'_id': player_id})
            if player:
                players.append({'_id': str(get(player, '_id')), 'name': get(player, 'name')})
        set_(team, 'players', players)
        return {'context': 'team', 'method': 'get_team_with_player', 'data': team, 'code': 200}
    except Exception as e:
        return {'context': 'team', 'method': 'get_team_with_player', 'error': str(e), 'code': 500}


def get_team(team_id):
    try:
        team_collection = database_connection()['teams']
        try:
            team = team_collection.find_one({'_id': ObjectId(team_id)})
        except Exception as e:
            team = team_collection.find_one({'external_id': int(team_id)})
        if not team:
            return {'context': 'team', 'method': 'get_team', 'error': 'TEAM_NOT_FOUND', 'code': 404}
        set_(team, '_id', str(get(team, '_id', '')))
        return {'context': 'team', 'method': 'get_team', 'data': team, 'code': 200}
    except Exception as e:
        return {'context': 'team', 'method': 'get_team', 'error': str(e), 'code': 500}
