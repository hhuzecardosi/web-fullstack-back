from datetime import datetime, timedelta
from bson import ObjectId
from pydash.objects import get, set_

from database.database_connection import database_connection
from common.utils import create_deck, difference_in_dates, transform_deck_to_export, transform_blacklist_to_export
from components.nba.game import get_games_by_date


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
        date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        if len(players) == 0:
            return {'context': 'player', 'method': 'get_player', 'error': 'PLAYER_NOT_FOUND', 'code': 404}
        games = get_games_by_date(date)
        while get(games, 'error', '') == 'NO_GAME_FOUND':
            print(date)
            date = datetime.strptime(date, '%Y-%m-%d')
            date = (date - timedelta(days=1)).strftime('%Y-%m-%d')
            games = get_games_by_date(date)
        # print(date)
        night_players = []
        for p in players:
            statistics = get_statistics_from_date(date, player=p)
            if statistics:
                night_players.append({'_id': str(p['_id']), 'name': p['name'], 'stats': statistics})
        return {'context': 'player', 'method': 'get_player', 'data': night_players, 'code': 200}
    except Exception as e:
        return {'context': 'player', 'method': 'get_player', 'error': str(e), 'code': 500}


def get_statistics_from_date(string_date, player):
    try:
        date = datetime.strptime(string_date, '%Y-%m-%d')
        statistics = next((stats for i, stats in enumerate(get(player, 'stats')) if stats['date'] == date), None)
        if statistics:
            statistics['date'] = '' if get(statistics, 'date', '') == '' else get(statistics, 'date').strftime('%Y-%m-%d')
        return statistics
    except Exception as e:
        print(e)
        return []


def pick_player(user_id, player_id, pick_date):
    try:
        date = datetime.strptime(pick_date, '%Y-%m-%d')
        print(difference_in_dates(date, datetime.now()))
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

        blacklist_index = next((i for i, blacklist in enumerate(get(user, 'blacklist', []))
                                if get(blacklist, 'player') == player['_id']), -1)
        print(blacklist_index)
        if blacklist_index >= 0:
            return {'context': 'player', 'method': 'pick_player', 'error': 'PLAYER_IN_BLACKLIST', 'code': 400}

        deck_ = create_deck(pick_date)
        deck_index = next((i for i, deck in enumerate(get(user, 'decks', []))
                           if get(deck, 'from', '') == deck_['from'] and get(deck, 'to', '') == deck_['to']), -1)
        print('deck_index', deck_index)
        if deck_index == -1:
            user['decks'].append(deck_)
            deck_index = 0

        choice_index = next((i for i, choice in enumerate(get(user, 'decks.' + str(deck_index) + '.choices', []))
                             if get(choice, 'date') == date), -1)

        print('choice_index', choice_index)
        if choice_index == -1:
            choice = {'date': date, 'player': ObjectId(player_id)}
            deck = get(user, 'decks.' + str(deck_index))
            deck['choices'].append(choice)
            set_(user, 'decks.' + str(deck_index), deck)
            user['blacklist'].append({'since': date, 'to': date + timedelta(days=7), 'player': ObjectId(player_id)})
        else:
            old_choice = get(user, 'decks.' + str(deck_index) + '.choices.' + str(choice_index))
            print('old_choice', old_choice)
            choice = {'date': date, 'player': ObjectId(player_id)}
            print('choice', choice)
            set_(user, 'decks.' + str(deck_index) + '.choices.' + str(choice_index), choice)
            print('choice 2', choice)
            blacklist_index = next((i for i, b in enumerate(get(user, 'blacklist', []))
                                    if old_choice['player'] == b['player']), -1)
            print('blacklist_index', blacklist_index)
            if blacklist_index == -1:
                user['blacklist'].append({'since': date, 'to': date + timedelta(days=7), player: ObjectId(player_id)})
            else:
                set_(user, 'blacklist.' + str(blacklist_index),
                     {'since': date, 'to': date + timedelta(days=7), player: ObjectId(player_id)})

        user_collection.update_one({'_id': ObjectId(user_id)}, {"$set": user})
        print('decks', get(user, 'decks.' + str(deck_index)))
        data = {'deck': transform_deck_to_export([get(user, 'decks.' + str(deck_index), [])]),
                'blacklist': transform_blacklist_to_export(get(user, 'blacklist', []))}
        return {'context': 'player', 'method': 'pick_player', 'data': data, 'code': 200}
    except Exception as e:
        print(e)
        return {'context': 'player', 'method': 'pick_player', 'error': str(e), 'code': 500}
