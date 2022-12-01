from flask_restplus import Resource, Namespace, fields
from flask import request, make_response
from components.user.user import register, sign_in, get_profile, update, update_password, get_deck, get_blacklist, \
    get_history
from pydash.objects import get

from jwt_check.jwt_check import token_required, decode_token

ns_user_endpoint = Namespace('api/user')
ns_endpoint = Namespace('api')

user_model = ns_user_endpoint.model('user', {
    'email': fields.String(required=True),
    'password': fields.String(),
    'pseudo': fields.String(),
    'decks': fields.String(),
    'blacklist': fields.String()
})
user_update_model = ns_user_endpoint.model('user_update', {
    'pseudo': fields.String()
})
user_password_update_model = ns_user_endpoint.model('user_password_update', {
    'password': fields.String(required=True),
    'new_password': fields.String(required=True)
})
register_model = ns_endpoint.model('register', {
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'pseudo': fields.String(required=True),
})
signin_model = ns_endpoint.model('sign in', {
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})


@ns_endpoint.route('/register')
class Register(Resource):
    @ns_endpoint.expect(register_model)
    @ns_endpoint.response(201, 'Successfully registered')
    @ns_endpoint.response(400, 'Data error')
    @ns_endpoint.response(500, 'Internal server error')
    def post(self):
        try:
            data = request.json
            result = register(data['email'], data['password'], data['pseudo'])
            return make_response(result, result['code'])
        except Exception as e:
            print(e)
            return make_response({'context': '', 'method': 'register', 'error': str(e), 'code': 500}, 500)


@ns_endpoint.route('/signin')
class SignIn(Resource):
    @ns_endpoint.expect(signin_model)
    @ns_endpoint.response(200, 'Successfully registered')
    @ns_endpoint.response(401, 'Data error')
    @ns_endpoint.response(500, 'Internal server error')
    def post(self):
        try:
            data = request.json
            result = sign_in(data['email'], data['password'])
            return make_response(result, result['code'])
        except Exception as e:
            print(e)
            return make_response({'context': '', 'method': 'signin', 'error': str(e), 'code': 500}, 500)


@ns_user_endpoint.route('/<string:user_id>')
class User(Resource):
    @token_required
    @ns_user_endpoint.response(200, 'Success')
    @ns_user_endpoint.response(404, 'Not Found')
    @ns_user_endpoint.response(500, 'Internal server error')
    def get(self, user_id):
        try:
            result = get_profile(user_id)
            return make_response(result, result['code'])
        except Exception as e:
            print(e)
            return make_response({'context': 'user', 'method': 'get', 'error': str(e), 'code': 500}, 500)

    @token_required
    @ns_user_endpoint.expect(user_update_model)
    @ns_user_endpoint.response(200, 'Success')
    @ns_user_endpoint.response(404, 'Not Found')
    @ns_user_endpoint.response(500, 'Internal server error')
    def put(self, user_id):
        try:
            result = update(user_id, request.json)
            return make_response(result, result['code'])
        except Exception as e:
            print(e)
            return make_response({'context': 'user', 'method': 'put', 'error': str(e), 'code': 500}, 500)


@ns_user_endpoint.route('/password/<string:user_id>')
class UserPassword(Resource):
    @token_required
    @ns_user_endpoint.expect(user_password_update_model)
    @ns_user_endpoint.response(200, 'Success')
    @ns_user_endpoint.response(404, 'User Not Found')
    @ns_user_endpoint.response(500, 'Internal server error')
    def put(self, user_id):
        try:
            data = request.json
            old_password = get(data, 'password', '')
            new_password = get(data, 'new_password', '')
            if old_password == '' or new_password == '':
                return make_response({'context': 'user', 'method': 'change_password', 'error': 'PASSWORDS_EMPTY',
                                      'code': 400}, 400)
            result = update_password(user_id, old_password, new_password)
            return make_response(result, result['code'])
        except Exception as e:
            print(e)
            return make_response({'context': 'user', 'method': 'change_password', 'error': str(e), 'code': 500}, 500)


@ns_user_endpoint.route('/deck')
class Deck(Resource):
    @token_required
    @ns_user_endpoint.response(200, 'Success')
    @ns_user_endpoint.response(404, 'User Not Found')
    @ns_user_endpoint.response(500, 'Internal server error')
    def get(self):
        try:
            token = decode_token(request.headers.get("Authorization"))
            result = get_deck(get(token, 'user_id'))
            return make_response(result, result['code'])
        except Exception as e:
            print(e)
            return make_response({'context': 'user', 'method': 'get_deck', 'error': str(e), 'code': 500}, 500)


@ns_user_endpoint.route('/history')
class Deck(Resource):
    @token_required
    @ns_user_endpoint.response(200, 'Success')
    @ns_user_endpoint.response(404, 'User Not Found')
    @ns_user_endpoint.response(500, 'Internal server error')
    def get(self):
        try:
            token = decode_token(request.headers.get("Authorization"))
            result = get_history(get(token, 'user_id'))
            return make_response(result, result['code'])
        except Exception as e:
            print(e)
            return make_response({'context': 'user', 'method': 'get_deck', 'error': str(e), 'code': 500}, 500)


@ns_user_endpoint.route('/blacklist')
class Deck(Resource):
    @token_required
    @ns_user_endpoint.response(200, 'Success')
    @ns_user_endpoint.response(404, 'User Not Found')
    @ns_user_endpoint.response(500, 'Internal server error')
    def get(self):
        try:
            token = decode_token(request.headers.get("Authorization"))
            result = get_blacklist(get(token, 'user_id'))
            return make_response(result, result['code'])
        except Exception as e:
            print(e)
            return make_response({'context': 'user', 'method': 'get_deck', 'error': str(e), 'code': 500}, 500)
