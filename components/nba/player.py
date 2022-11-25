from datetime import datetime, timedelta
from bson import ObjectId
from pydash.objects import get, set_

from database.database_connection import database_connection
from common.utils import create_deck, difference_in_dates


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
                night_players.append({'_id': p['_id'], 'name': p['name'], 'stats': statistics[0]})
        return {'context': 'player', 'method': 'get_player', 'data': night_players, 'code': 200}
    except Exception as e:
        return {'context': 'player', 'method': 'get_player', 'error': str(e), 'code': 500}


def pick_player(user_id, player_id, pick_date):
    try:
        date = datetime.strptime(pick_date, '%Y-%m-%d')
        if difference_in_dates(date, datetime.now()) < 0:
            return {'context': 'player', 'method': 'pick_player', 'error': 'DATE_PASSED', 'code': 400}
        user_collection = database_connection()['users']
        player_collection = database_connection()['players']
        user = user_collection.find_one({'_id': ObjectId(user_id)})
        player = player_collection.find_one({'_id': ObjectId(player_id)})
        if not user:
            return {'context': 'player', 'method': 'pick_player', 'error': 'USER_NOT_FOUND', 'code': 404}
        if not player:
            return {'context': 'player', 'method': 'pick_player', 'error': 'PLAYER_NOT_FOUND', 'code': 404}
        blacklist_index = [i for i, blacklist in enumerate(get(user, 'blacklist', []))
                           if get(blacklist, 'player') == player['_id']][0]
        if blacklist_index >= 0:
            return {'context': 'player', 'method': 'pick_player', 'error': 'PLAYER_IN_BLACKLIST', 'code': 400}

        deck = create_deck(pick_date)
        deck_index = next((i for i, deck in enumerate(get(user, 'decks', []))
                           if get(deck, 'from', '') == deck['from'] and get(deck, 'to', '') == deck['to']), -1)

        if deck_index == -1:
            user['decks'].append(deck)
            deck_index = 0

        choice_index = next((i for i, choice in enumerate(get(user, 'decks.' + str(deck_index) + '.choices', []))
                             if get(choice, 'date') == date), -1)

        if choice_index == -1:
            choice = {'date': date, 'player': ObjectId(player_id)}
            deck = get(user, 'decks.' + str(deck_index))
            deck['choices'].append(choice)
            set_(user, 'decks.' + str(deck_index), deck)
            user['blacklist'].append({'since': date, 'to': date + timedelta(days=7), player: ObjectId(player_id)})
        else:
            old_choice = get(user, 'decks.' + str(deck_index) + '.choices.' + str(choice_index))
            choice = {'date': date, 'player': ObjectId(player_id)}
            set_(user, 'decks.' + str(deck_index) + '.choices.' + str(choice_index), choice)
            blacklist_index = next((i for i, b in enumerate(get(user, 'blacklist', []))
                                    if old_choice['player'] == b['player']), -1)
            if blacklist_index == -1:
                user['blacklist'].append({'since': date, 'to': date + timedelta(days=7), player: ObjectId(player_id)})
            else:
                set_(user, 'blacklist.' + str(blacklist_index),
                     {'since': date, 'to': date + timedelta(days=7), player: ObjectId(player_id)})
        user_collection.update_one({'_id': user_id}, {"$set": user})
        data = {'deck': get(user, 'decks.' + str(deck_index), []), 'blacklist': get(user, 'blacklist', [])}
        return {'context': 'player', 'method': 'pick_player', 'data': data, 'code': 200}
    except Exception as e:
        print(e)
        return {'context': 'player', 'method': 'pick_player', 'error': str(e), 'code': 500}
