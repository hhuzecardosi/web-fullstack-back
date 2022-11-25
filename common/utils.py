from pydash.objects import get, set_
from datetime import datetime, timedelta


def difference_in_dates(date1, date2):
    diff = date1 - date2
    return diff.total_seconds() / (60 * 60 * 24)


def compute_player_stats(game, player):
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
    return db_stats


def create_deck(string_date):
    date = datetime.strptime(string_date, '%Y-%m-%d')
    day = date.weekday()
    return {'from': date - timedelta(days=day), 'to': date + timedelta(days=(6 - day)), 'choices': []}


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
