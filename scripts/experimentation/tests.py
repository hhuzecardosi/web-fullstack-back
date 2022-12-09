from common.utils import get_all_path
from bson import ObjectId

a = {
    "_id" : ObjectId('6375fb83af475654d23d6047'),
    "external_id" : 1629029,
    "name" : "Luka Doncic",
    "number" : "77",
    "team" : ObjectId('6375fb14af475654d23d5fcb'),
    "stats" : [
        {
            "gameId" : "0022200172",
            "date" : '2022-11-10T00:00:00.000Z'
        }
    ]
}

# print(get_all_path('', a))

b = {
    'list_in_list': [
        ['element0.0', 'element0.1'],
        ['element1.0', 'element1.1'],
        []
    ]
}
# print(get_all_path('', b))


print(type(ObjectId("637f7cc7e95b6228261ade0c")))
