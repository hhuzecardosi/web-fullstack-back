from nba_api.live.nba.endpoints import boxscore
from nba_api.live.nba.endpoints import scoreboard
from pydash.objects import get, set_
from datetime import datetime

from database.database_connection import database_connection
from common.utils import difference_in_dates, compute_player_stats, create_deck


def daily_update(string_date):
    try:
        print('\nDaily Update ', string_date)
        player_collection = database_connection()['players']
        team_collection = database_connection()['teams']
        game_collection = database_connection()['games']
        user_collection = database_connection()['users']
        game_date = datetime.strptime(string_date, '%Y-%m-%d')
        # print('Game Date', game_date)
        games = list(game_collection.find({'date': game_date}))

        choices = []
        users = list(user_collection.find())

        # Users update
        for user in users:
            # Choices count
            deck = create_deck(string_date)
            deck_index = next((i for (i, deck) in enumerate(get(user, 'decks', []))
                               if get(deck, 'from', '') == create_deck(string_date)['from']
                               and get(deck, 'to', '') == create_deck(string_date)['to']), -1)
            if deck_index != -1:
                deck = get(user, 'decks.' + str(deck_index))
                choice_index = next(
                    (i for i, choice in enumerate(get(user, 'decks.' + str(deck_index) + '.choices', []))
                     if get(choice, 'date') == game_date), -1)
                if choice_index != -1:
                    choices.append(get(user, 'decks.' + str(deck_index) + '.choices.' + str(choice_index)))

            # Blacklist handle
            blacklist = []
            for player in get(user, 'blacklist', []):
                if game_date < player['to']:
                    blacklist.append(player)
            set_(user, 'blacklist', blacklist)
            user_collection.update_one({'_id': user['_id']}, {'$set': user})

        # print('choices', len(choices))

        # Players & Games update
        # print('Players & Games')
        # print('Games', games)
        for game in games:
            players = boxscore.BoxScore(get(game, 'external_id')).get_dict()
            get(players, 'game.homeTeam.players', [])
            update_players(player_collection, team_collection, string_date, get(players, 'game.homeTeam.players', []),
                           game, choices, get(players, 'game.homeTeam.teamId'))
            update_players(player_collection, team_collection, string_date, get(players, 'game.awayTeam.players', []),
                           game, choices, get(players, 'game.homeTeam.teamId'))
            game['status'] = 'FINAL'
            game['h_score'] = players['game']['homeTeam']['score']
            game['v_score'] = players['game']['awayTeam']['score']
            # print('Game : ', game)
            game_collection.update_one({'_id': game['_id']}, {'$set': game})
        return True
    except Exception as e:
        print(e)
        return False


def update_players(player_collection, team_collection, string_date, players, game, choices, team_external_id):
    try:
        for player in players:
            print(player['name'])
            db_player = player_collection.find_one({'external_id': get(player, 'personId')})
            if not db_player:
                print('Player not in database')
                team = team_collection.find_one({'external_id': team_external_id})
                db_player = {'external_id': player['personId'], 'name': player['name'], 'number': player['jerseyNum'],
                             'team': team['_id'], 'stats': []}
                player_collection.insert_one(db_player)
                db_player = player_collection.find_one({'external_id': get(player, 'personId')})
            stats_index = next((i for i, stats in enumerate(get(db_player, 'stats', []))
                                if stats['date'].strftime('%Y-%m-%d') == string_date), -1)
            player_stats = compute_player_stats(game, player)
            player_pick = len([i for i, choice in enumerate(choices) if choice == get(db_player, '_id')])
            set_(player_stats, 'picks', player_pick)
            if stats_index != -1:
                set_(db_player, 'stats.' + str(stats_index), player_stats)
            else:
                db_player['stats'].append(player_stats)
            player_collection.update_one({'_id': db_player['_id']}, {'$set': db_player})
    except Exception as e:
        print('update players', e)
