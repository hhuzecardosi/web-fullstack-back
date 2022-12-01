from flask_restplus import Resource, Api
from .user_endpoints import ns_user_endpoint as user
from .user_endpoints import ns_endpoint
from .nba_endpoints import ns_game_endpoint as game
from .nba_endpoints import ns_player_endpoint as player
from .nba_endpoints import ns_team_endpoint as team

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
}
api = Api(
    title='NBA Fantasy League',
    version='1.0',
    description='Various orchestration for a NBA Fantasy League app',
    # All API metadatas
    security='Bearer Auth',
    authorizations=authorizations
)

api.add_namespace(ns_endpoint)
api.add_namespace(user)
api.add_namespace(ns_endpoint)
api.add_namespace(game)
api.add_namespace(team)
api.add_namespace(player)
