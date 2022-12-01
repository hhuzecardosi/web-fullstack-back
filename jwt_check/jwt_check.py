from functools import wraps
from flask import request, make_response
import jwt
from bson import ObjectId

from common.config_utils import get_config_json
from database import database_connection


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        users_collection = database_connection.database_connection()['users']
        token = request.headers.get("Authorization")
        if not token:
            return make_response({'message': 'MISSING_TOKEN'}, 403)
        try:
            token = token.split(" ")[1]
            payload = jwt.decode(token, get_config_json('globals')['secret_key'], algorithms=['HS256'])
            user = users_collection.find_one({'_id': ObjectId(payload['user_id'])})
            if not user:
                return make_response({'error': 'INVALID_TOKEN'}, 403)
            if user['email'] != payload['user_email']:
                return make_response({'error': 'UNAUTHORIZED_USER'}, 409)
        except Exception as e:
            print("Error in token :", str(e))
            return make_response({'error': 'INVALID_TOKEN'}, 403)
        return f(*args, **kwargs)

    return decorated


def decode_token(token):
    token = token.split(" ")[1]
    return jwt.decode(token, get_config_json('globals')['secret_key'], algorithms=['HS256'])
