import bcrypt
import jwt
from pydash.objects import get, set_
from bson import ObjectId

from common.config_utils import get_config_json
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
        new_user = {
            'email': email,
            'pseudo': pseudo,
            'password': password,
            'decks': [],
            'blacklist': []
        }
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
        set_(user, 'password', '')
        set_(user, '_id', str(user['_id']))
        data = {'token': token, 'user': user}
        return {'context': 'user', 'method': 'signin', 'data': data, 'code': 200}
    except Exception as e:
        print(e)
        return {'context': 'user', 'method': 'signin', 'error': str(e), 'code': 500}


def update(user, pseudo):
    try:
        client_collection = database_connection.database_connection()['users']
        return {'data': {}, 'code': 200}
    except Exception as e:
        print(e)
        return {'context': 'user', 'method': 'update', 'error': str(e), 'code': 500}


def update_password(user, old_password, new_password):
    try:
        user_collection = database_connection.database_connection()['users']
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
        return {'context': 'user', 'method': 'get_profile', 'data': user, 'code': 200}
    except Exception as e:
        print(e)
        return {'context': 'user', 'method': 'get_profile', 'error': str(e), 'code': 500}


def get_deck(user, from_, to):
    try:
        user_collection = database_connection.database_connection()['users']
        return {'data': '', 'code': 200}
    except Exception as e:
        print(e)
        return {'context': 'user', 'method': 'get_deck', 'error': str(e), 'code': 500}


def get_history(user):
    try:
        user_collection = database_connection.database_connection()['users']
        return {'data': '', 'code': 200}
    except Exception as e:
        print(e)
        return {'context': 'user', 'method': 'get_history', 'error': str(e), 'code': 500}


def get_blacklist(user):
    try:
        user_collection = database_connection.database_connection()['users']
        return {'data': '', 'code': 200}
    except Exception as e:
        print(e)
        return {'context': 'user', 'method': 'get_blacklist', 'error': str(e), 'code': 500}
