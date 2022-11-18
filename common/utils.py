from pydash.objects import get, set_


def difference_in_dates(date1, date2):
    diff = date1 - date2
    return diff.total_seconds() / (60 * 60 * 24)


def compute_player_stats(player_collection, game, player):
    external_id = player['personId']
    db_player = player_collection.find_one({'external_id': external_id})
    if db_player:
        statistics = player['statistics']
        db_stats = {
            'gameId': game['external_id'],
            'date': game['date'],
            'points': statistics['points'],
            'assists': statistics['assists'],
            'rebounds': statistics['reboundsTotal'],
            'blocks': statistics['blocks'],
            'steals': statistics['steals'],
            'ftm': statistics['freeThrowsMade'],
            'fgm': statistics['fieldGoalsMade'],
            'fg3m': statistics['threePointersMade'],
            'fta': statistics['freeThrowsAttempted'],
            'fga': statistics['fieldGoalsAttempted'],
            'fg3a': statistics['threePointersAttempted'],
            'turnovers': statistics['turnovers']
        }
        plus = db_stats['points'] + db_stats['assists'] + db_stats['rebounds'] \
               + db_stats['blocks'] + db_stats['ftm'] + db_stats['fgm'] + db_stats['fg3m'] + db_stats['steals']
        minus = (db_stats['fga'] - db_stats['fgm']) + (db_stats['fta'] - db_stats['ftm']) \
                + (db_stats['fg3a'] - db_stats['fg3m'] + db_stats['turnovers'])
        db_stats['plus'] = plus
        db_stats['minus'] = minus
        db_stats['score'] = plus - minus
        db_player['stats'].append(db_stats)
        player_collection.update_one({'external_id': external_id}, {'$set': db_player})
        return True
    return False


def update_changes(old_dict, new_dict):
    paths = get_all_path('', old_dict)
    for p in paths:
        print(type(get(old_dict, p)))
        # TODO check if values are the same (exception for the list, dict and date)
    return True


def get_all_path(path, object):
    paths = []
    for i, k in enumerate(object):
        key = k
        if str(type(object)) == "<class 'list'>":
            key = i
        key_path = path + '.' + str(key) if path != '' else str(key)
        paths.append(key_path)
        if str(type(object[key])) == "<class 'list'>":
            for item in enumerate(object[key]):
                if str(type(item[1])) == "<class 'dict'>" or str(type(item[1])) == "<class 'list'>":
                    sub_paths = get_all_path(str(key) + '.' + str(item[0]), item[1])
                    paths.extend(sub_paths)
                else:
                    paths.append(key_path + '.' + str(item[0]))
        elif str(type(object[key])) == "<class 'dict'>":
            sub_paths = get_all_path(key_path, object[key])
            paths.extend(sub_paths)
    return paths
