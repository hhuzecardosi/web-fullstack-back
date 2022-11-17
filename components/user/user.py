import bcrypt
import jwt
from pydash.objects import get, set_

from common.config_utils import get_config_json
from database import database_connection


def register(email, password, pseudo):
    try:
        client_collection = database_connection.database_connection()['users']
        user = client_collection.find_one({'email': email})
        if user:
            return {'context': 'user', 'method': 'create', 'error': 'EMAIL_ALREADY_USED', 'code': 400}
        user = client_collection.find_one({'pseudo': pseudo})
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
        client_collection.insert_one(new_user)
        return {'context': 'user', 'method': 'create', 'code': 201}
    except Exception as e:
        print(e)
        return {'context': 'user', 'method': 'create', 'error': str(e), 'code': 500}


def sign_in(email, password):
    try:
        client_collection = database_connection.database_connection()['users']
        user = client_collection.find_one({'email': email})
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
        data = {'token': token}
        return {'context': 'user', 'method': 'signin', 'data': data, 'code': 200}
    except Exception as e:
        print(e)
        return {'context': 'user', 'method': 'signin', 'error': str(e), 'code': 500}


def update(user, pseudo):
    try:
        client_collection = database_connection.database_connection()['users']
        return {'data': '', 'code': 200}
    except Exception as e:
        print(e)
        return {'context': 'user', 'method': 'update', 'error': str(e), 'code': 500}


def update_password(user, old_password, new_password):
    try:
        client_collection = database_connection.database_connection()['users']
        return {'data': '', 'code': 200}
    except Exception as e:
        print(e)
        return {'context': 'user', 'method': 'update_password', 'error': str(e), 'code': 500}


def get_profile(user):
    try:
        client_collection = database_connection.database_connection()['users']
        return {'data': '', 'code': 200}
    except Exception as e:
        print(e)
        return {'context': 'user', 'method': 'get_profile', 'error': str(e), 'code': 500}


def get_deck(user, from_, to):
    try:
        client_collection = database_connection.database_connection()['users']
        return {'data': '', 'code': 200}
    except Exception as e:
        print(e)
        return {'context': 'user', 'method': 'get_deck', 'error': str(e), 'code': 500}


def get_history(user):
    try:
        client_collection = database_connection.database_connection()['users']
        return {'data': '', 'code': 200}
    except Exception as e:
        print(e)
        return {'context': 'user', 'method': 'get_history', 'error': str(e), 'code': 500}


def get_blacklist(user):
    try:
        client_collection = database_connection.database_connection()['users']
        return {'data': '', 'code': 200}
    except Exception as e:
        print(e)
        return {'context': 'user', 'method': 'get_blacklist', 'error': str(e), 'code': 500}