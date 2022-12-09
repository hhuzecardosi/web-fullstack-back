import json

from bson import json_util
from pydash.objects import get, set_
from datetime import datetime, timedelta
from database.database_connection import database_connection


def difference_in_dates(date1, date2):
    diff = date1 - date2
    return diff.total_seconds() / (60 * 60 * 24)


def compute_player_stats(game, player):
    statistics = player['statistics']
    db_stats = {
        'gameId': game['external_id'],
        'date': game['date'],
        'points': statistics['points'],
        'assists': statistics['assists'],
        'rebounds': statistics['reboundsTotal'],
        'blocks': statistics['blocks'],
        'steals': statistics['steals'],
        'ftm': statistics['freeThrowsMade'],
        'fgm': statistics['fieldGoalsMade'],
        'fg3m': statistics['threePointersMade'],
        'fta': statistics['freeThrowsAttempted'],
        'fga': statistics['fieldGoalsAttempted'],
        'fg3a': statistics['threePointersAttempted'],
        'turnovers': statistics['turnovers']
    }
    plus = db_stats['points'] + db_stats['assists'] + db_stats['rebounds'] \
           + db_stats['blocks'] + db_stats['ftm'] + db_stats['fgm'] + db_stats['fg3m'] + db_stats['steals']
    minus = (db_stats['fga'] - db_stats['fgm']) + (db_stats['fta'] - db_stats['ftm']) \
            + (db_stats['fg3a'] - db_stats['fg3m'] + db_stats['turnovers'])
    db_stats['plus'] = plus
    db_stats['minus'] = minus
    db_stats['score'] = plus - minus
    return db_stats


def create_deck(string_date):
    date = datetime.strptime(string_date, '%Y-%m-%d')
    day = date.weekday()
    return {'from': date - timedelta(days=day), 'to': date + timedelta(days=(6 - day)), 'choices': []}


def get_all_path(path, object):
    paths = []
    for i, k in enumerate(object):
        key = k
        if str(type(object)) == "<class 'list'>":
            key = i
        key_path = path + '.' + str(key) if path != '' else str(key)
        paths.append(key_path)
        if str(type(object[key])) == "<class 'list'>":
            for item in enumerate(object[key]):
                if str(type(item[1])) == "<class 'dict'>" or str(type(item[1])) == "<class 'list'>":
                    sub_paths = get_all_path(str(key) + '.' + str(item[0]), item[1])
                    paths.extend(sub_paths)
                else:
                    paths.append(key_path + '.' + str(item[0]))
        elif str(type(object[key])) == "<class 'dict'>":
            sub_paths = get_all_path(key_path, object[key])
            paths.extend(sub_paths)
    return paths


def transform_deck_to_export(decks):
    print('transform_deck_to_export')
    player_collection = database_connection()['players']
    transformed_deck = []
    for deck in decks:
        from_date = '' if get(deck, 'from', '') == '' else get(deck, 'from').strftime('%Y-%m-%d')
        to_date = '' if get(deck, 'to', '') == '' else get(deck, 'to').strftime('%Y-%m-%d')
        d = {'from': from_date, 'to': to_date, 'choices': []}
        for choice in get(deck, 'choices', []):
            player = player_collection.find_one({'_id': get(choice, 'player')})
            player = {'name': get(player, 'name'), '_id': str(get(choice, 'player'))}
            string_date = '' if get(choice, 'date', '') == '' else get(choice, 'date').strftime('%Y-%m-%d')
            c = {'player': player, 'date': string_date}
            d['choices'].append(c)
        transformed_deck.append(d)
    return transformed_deck


def transform_blacklist_to_export(blacklist):
    print('blacklist')
    player_collection = database_connection()['players']
    transformed_blacklist = []
    for blacklisted in blacklist:
        player_db = player_collection.find_one({'_id': get(blacklisted, 'player')})
        player_db = {'name': get(player_db, 'name'), '_id': str(get(blacklisted, 'player'))}
        transformed_blacklist.append({'player': player_db,
                                      'since': get(blacklisted, 'since').strftime('%Y-%m-%d'),
                                      'to': get(blacklisted, 'to').strftime('%Y-%m-%d')})
    return transformed_blacklist


def transform_games_to_export(data):
    for game in data:
        game['_id'] = str(game['_id'])
        game['h_team'] = str(game['h_team']) if str(type(game['h_team'])) == "<class 'bson.objectid.ObjectId'>" else game['h_team']
        game['v_team'] = str(game['v_team']) if str(type(game['v_team'])) == "<class 'bson.objectid.ObjectId'>" else game['v_team']
        game['date'] = game['date'].strftime('%Y-%m-%d')
    return data
