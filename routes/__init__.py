from flask_restplus import Resource, Api
from .user_endpoints import ns_user_endpoint as user
from .user_endpoints import ns_endpoint

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

api.add_namespace(user)
api.add_namespace(ns_endpoint)
