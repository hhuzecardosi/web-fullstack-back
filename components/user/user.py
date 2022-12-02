import bcrypt
import jwt
from pydash.objects import get, set_
from bson import ObjectId
from datetime import datetime

from common.config_utils import get_config_json
from common.utils import create_deck, difference_in_dates, transform_deck_to_export, transform_blacklist_to_export
from database import database_connection


def register(email, password, pseudo):
    try:
        user_collection = database_connection.database_connection()['users']
        user = user_collection.find_one({'email': email})
        if user:
            return {'context': 'user', 'method': 'create', 'error': 'EMAIL_ALREADY_USED', 'code': 400}
        user = user_collection.find_one({'pseudo': pseudo})
        if user:
            return {'context': 'user', 'method': 'create', 'error': 'PSEUDO_ALREADY_USED', 'code': 400}
        b_password = password.encode('utf-8')
        password = bcrypt.hashpw(b_password, bcrypt.gensalt())
        from_to = create_deck(datetime.now().strftime('%Y-%m-%d'))
        deck = {'from': from_to['from'], 'to': from_to['to'], 'choices': []}
        new_user = {'email': email, 'pseudo': pseudo, 'password': password, 'decks': [deck], 'blacklist': []}
        user_collection.insert_one(new_user)
        return {'context': 'user', 'method': 'create', 'code': 201}
    except Exception as e:
        print(e)
        return {'context': 'user', 'method': 'create', 'error': str(e), 'code': 500}


def sign_in(email, password):
    try:
        user_collection = database_connection.database_connection()['users']
        user = user_collection.find_one({'email': email})
        if not user:
            return {'context': 'user', 'method': 'signin', 'error': 'UNAUTHORIZED', 'code': 401}
        b_password = str(password).encode('utf-8')
        if not bcrypt.checkpw(b_password, user['password']):
            return {'context': 'user', 'method': 'signin', 'error': 'UNAUTHORIZED', 'code': 401}
        # token creation
        token_expiry = get_config_json('globals')['token_expiry']
        secret_key = get_config_json('globals')['secret_key']
        payload = {'user_email': user['email'], 'user_id': str(user['_id']), 'expiry': token_expiry}
        token = jwt.encode(payload=payload, key=secret_key)
        set_(user, '_id', str(user['_id']))
        data = {'token': token, 'user': {'_id': user['_id'], 'email': user['email'], 'pseudo': user['pseudo']}}
        return {'context': 'user', 'method': 'signin', 'data': data, 'code': 200}
    except Exception as e:
        print(e)
        return {'context': 'user', 'method': 'signin', 'error': str(e), 'code': 500}


def update(user, data):
    try:
        user_collection = database_connection.database_connection()['users']
        user = user_collection.find_one({'_id': ObjectId(user)})
        if not user:
            return {'context': 'user', 'method': 'get_profile', 'error': 'USER_NOT_FOUND', 'code': 404}
        user_collection.update_one({'_id': ObjectId(user)})
        return {'data': {}, 'code': 200}
    except Exception as e:
        print(e)
        return {'context': 'user', 'method': 'update', 'error': str(e), 'code': 500}


def update_password(user_id, old_password, new_password):
    try:
        user_collection = database_connection.database_connection()['users']
        user = user_collection.find_one({'_id': ObjectId(user_id)})
        if not user:
            return {'context': 'user', 'method': 'get_profile', 'error': 'USER_NOT_FOUND', 'code': 404}
        b_password = str(old_password).encode('utf-8')
        if not bcrypt.checkpw(b_password, user['password']):
            return {'context': 'user', 'method': 'signin', 'error': 'WRONG_PASSWORD', 'code': 401}
        b_password = new_password.encode('utf-8')
        password = bcrypt.hashpw(b_password, bcrypt.gensalt())
        set_(user, 'password', str(password))
        user_collection.update_one({'_id': ObjectId(user_id)}, {'$set': user})
        return {'data': '', 'code': 200}
    except Exception as e:
        print(e)
        return {'context': 'user', 'method': 'update_password', 'error': str(e), 'code': 500}


def get_profile(user):
    try:
        user_collection = database_connection.database_connection()['users']
        user = user_collection.find_one({'_id': ObjectId(user)})
        if not user:
            return {'context': 'user', 'method': 'get_profile', 'error': 'USER_NOT_FOUND', 'code': 404}
        user['password'] = ''
        user['_id'] = str(user['_id'])
        user['decks'] = transform_deck_to_export(user['decks'])
        user['blacklist'] = transform_blacklist_to_export(user['blacklist'])
        return {'context': 'user', 'method': 'get_profile', 'data': user, 'code': 200}
    except Exception as e:
        print(e)
        return {'context': 'user', 'method': 'get_profile', 'error': str(e), 'code': 500}


def get_deck(user_id):
    try:
        user_collection = database_connection.database_connection()['users']
        user = user_collection.find_one({'_id': ObjectId(user_id)})
        if not user:
            return {'context': 'user', 'method': 'get_deck', 'error': 'USER_NOT_FOUND', 'code': 404}
        string_date = datetime.now().strftime('%Y-%m-%d')
        deck_ = create_deck(string_date)
        deck_index = next((i for i, deck in enumerate(get(user, 'decks', []))
                           if get(deck, 'from', '').strftime('%Y-%m-%d') == deck_['from'].strftime('%Y-%m-%d')
                           and get(deck, 'to', '').strftime('%Y-%m-%d') == deck_['to'].strftime('%Y-%m-%d')), -1)
        if deck_index == -1:
            user_id['decks'].append(deck_)
            user_collection.update_one({'_id': user_id}, {'$set': user})
            return {'context': 'user', 'method': 'get_deck', 'data': user['decks'][0], 'code': 200}
        else:
            return {'context': 'user', 'method': 'get_deck',
                    'data': transform_deck_to_export([get(user, 'decks.' + str(deck_index))]), 'code': 200}
    except Exception as e:
        print(e)
        return {'context': 'user', 'method': 'get_deck', 'error': str(e), 'code': 500}


def get_history(user):
    try:
        user_collection = database_connection.database_connection()['users']
        player_collection = database_connection.database_connection()['players']
        user = user_collection.find_one({'_id': ObjectId(user)})
        if not user:
            return {'context': 'user', 'method': 'get_history', 'error': 'USER_NOT_FOUND', 'code': 404}
        players = []
        for deck in get(user, 'decks', []):
            for choice in get(deck, 'choices', []):
                date = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
                if difference_in_dates(choice['date'], date) < 0:
                    player = player_collection.find_one({'_id': ObjectId(get(choice, 'player', ''))})
                    if player:
                        statistics = [stats for i, stats in enumerate(get(player, 'stats'))
                                      if stats['date'] == get(choice, 'date')]
                        statistics = statistics[0]
                        statistics['date'] = '' if get(statistics, 'date', '') == '' else \
                            get(statistics, 'date').strftime('%Y-%m-%d')
                        string_date = '' if get(choice, 'date', '') == '' else get(choice, 'date').strftime('%Y-%m-%d')
                        players.append({'date': string_date, 'player_name': player['name'], 'stats': statistics,
                                        'player_id': str(player['_id'])})
        return {'context': 'user', 'method': 'get_history', 'data': players, 'code': 200}
    except Exception as e:
        print(e)
        return {'context': 'user', 'method': 'get_history', 'error': str(e), 'code': 500}


def get_blacklist(user_id):
    try:
        user_collection = database_connection.database_connection()['users']
        user = user_collection.find_one({'_id': ObjectId(user_id)})
        if not user:
            return {'context': 'user', 'method': 'get_blacklist', 'error': 'USER_NOT_FOUND', 'code': 404}
        return {'context': 'user', 'method': 'get_blacklist',
                'data': transform_blacklist_to_export(get(user, 'blacklist')), 'code': 200}
    except Exception as e:
        print(e)
        return {'context': 'user', 'method': 'get_blacklist', 'error': str(e), 'code': 500}
