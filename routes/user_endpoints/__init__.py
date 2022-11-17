from flask_restplus import Resource, Namespace, fields
from flask import request, Response, stream_with_context
from components.user.user import register, sign_in
from pydash.objects import get

ns_user_endpoint = Namespace('user')
ns_endpoint = Namespace('')

user_model = ns_user_endpoint.model('user', {
    'email': fields.String(required=True),
    'password': fields.String(),
    'pseudo': fields.String(),
    'decks': fields.String(),
    'blacklist': fields.String()
})

register_model = ns_user_endpoint.model('register', {
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'pseudo': fields.String(required=True),
})

signin_model = ns_user_endpoint.model('sign in', {
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})


@ns_endpoint.route('/register')
class Register(Resource):
    @ns_user_endpoint.expect(register_model)
    @ns_user_endpoint.response(201, 'Successfully registered')
    @ns_user_endpoint.response(400, 'Data error')
    @ns_user_endpoint.response(500, 'Internal server error')
    def post(self):
        try:
            data = request.json
            result = register(data['email'], data['password'], data['pseudo'])
            code = result['code']
            if code == 200:
                return result, code
            return result, code
        except Exception as e:
            print(e)


@ns_endpoint.route('/signin')
class SignIn(Resource):
    @ns_user_endpoint.expect(signin_model)
    @ns_user_endpoint.response(200, 'Successfully registered')
    @ns_user_endpoint.response(401, 'Data error')
    @ns_user_endpoint.response(500, 'Internal server error')
    def post(self):
        try:
            data = request.json
            result = sign_in(data['email'], data['password'])
            code = result['code']
            if code == 200:
                return result, code
            return result, code
        except Exception as e:
            print(e)
