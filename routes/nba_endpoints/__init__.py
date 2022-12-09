from flask_restplus import Resource, Namespace, fields
from flask import request, make_response
from pydash.objects import get, set_
from datetime import datetime

from components.nba.game import get_games_by_date, get_night_results, get_games_of_the_week
from components.nba.player import get_player, get_night_stats, pick_player
from components.nba.team import get_team_with_player

from jwt_check.jwt_check import token_required, decode_token

ns_game_endpoint = Namespace('api/game')
ns_player_endpoint = Namespace('api/player')
ns_team_endpoint = Namespace('api/team')


@ns_team_endpoint.route('/<string:team_id>')
class Team(Resource):
    @ns_game_endpoint.response(200, 'Success')
    @ns_game_endpoint.response(500, 'Internal server Error')
    @ns_game_endpoint.response(404, 'Resource not Found')
    def get(self, team_id):
        try:
            result = get_team_with_player(team_id)
            return make_response(result, get(result, 'code', 400))
        except Exception as e:
            return make_response({'context': 'team', 'method': 'get', 'error': str(e), 'code': 500}, 500)


@ns_game_endpoint.route('/yesterday')
class Game(Resource):
    @ns_game_endpoint.response(200, 'Success')
    @ns_game_endpoint.response(500, 'Internal server error')
    @ns_game_endpoint.response(404, 'Bad Request')
    def get(self):
        try:
            result = get_night_results()
            return make_response(result, get(result, 'code', 400))
        except Exception as e:
            return make_response({'context': 'game', 'method': 'get', 'error': str(e), 'code': 500}, 500)


@ns_game_endpoint.route('/<string:string_date>')
class Game(Resource):
    @token_required
    @ns_game_endpoint.response(200, 'Success')
    @ns_game_endpoint.response(500, 'Internal server error')
    @ns_game_endpoint.response(404, 'Bad Request')
    def get(self, string_date):
        try:
            result = get_games_by_date(string_date)
            return make_response(result, get(result, 'code', 400))
        except Exception as e:
            return make_response({'context': 'game', 'method': 'get', 'error': str(e), 'code': 500}, 500)


@ns_game_endpoint.route('/week')
class Game(Resource):
    @token_required
    @ns_game_endpoint.response(200, 'Success')
    @ns_game_endpoint.response(500, 'Internal server error')
    @ns_game_endpoint.response(404, 'Bad Request')
    def get(self):
        try:
            now = datetime.now().strftime('%Y-%m-%d')
            result = get_games_of_the_week(now)
            return make_response(result, get(result, 'code', 400))
        except Exception as e:
            return make_response({'context': 'game', 'method': 'get', 'error': str(e), 'code': 500}, 500)


@ns_player_endpoint.route('/<string:player_id>')
class Player(Resource):
    @token_required
    @ns_game_endpoint.response(200, 'Success')
    @ns_game_endpoint.response(500, 'Internal server error')
    @ns_game_endpoint.response(404, 'Bad Request')
    def get(self, player_id):
        try:
            result = get_player(player_id)
            return make_response(result, get(result, 'code', 400))
        except Exception as e:
            return make_response({'context': 'player', 'method': 'get', 'error': str(e), 'code': 500}, 500)


@ns_player_endpoint.route('/statistics/yesterday')
class Player(Resource):
    @ns_game_endpoint.response(200, 'Success')
    @ns_game_endpoint.response(500, 'Internal server error')
    @ns_game_endpoint.response(404, 'Bad Request')
    def get(self):
        try:
            result = get_night_stats()
            return make_response(result, get(result, 'code', 400))
        except Exception as e:
            return make_response({'context': 'player', 'method': 'get_statistics', 'error': str(e), 'code': 500}, 500)


@ns_player_endpoint.route('/pick/<string:string_date>/<string:player_id>')
class Player(Resource):
    @token_required
    @ns_game_endpoint.response(200, 'Success')
    @ns_game_endpoint.response(500, 'Internal server error')
    @ns_game_endpoint.response(404, 'Bad Request')
    def get(self, player_id, string_date):
        try:
            token = decode_token(request.headers.get("Authorization"))
            result = pick_player(user_id=get(token, 'user_id'), player_id=player_id, pick_date=string_date)
            return make_response(result, get(result, 'code', 400))
        except Exception as e:
            return make_response({'context': 'player', 'method': 'get_statistics', 'error': str(e), 'code': 500}, 500)
