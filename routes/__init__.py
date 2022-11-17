from flask_restplus import Resource, Api

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
}
api = Api(
    title='RegMate Print ',
    version='1.0',
    description='Description for all RegMate html_report Review API',
    # All API metadatas
    security='Bearer Auth',
    authorizations=authorizations
)
