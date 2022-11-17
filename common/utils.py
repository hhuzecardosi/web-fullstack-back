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
            'ftm': statistics['freeThrowsMade'],
            'fgm': statistics['fieldGoalsMade'],
            'fg3m': statistics['threePointersMade'],
            'fta': statistics['freeThrowsAttempted'],
            'fga': statistics['fieldGoalsAttempted'],
            'fg3a': statistics['threePointersAttempted'],
            'turnovers': statistics['turnovers']
        }
        plus = db_stats['points'] + db_stats['assists'] + db_stats['rebounds'] \
               + db_stats['blocks'] + db_stats['ftm'] + db_stats['fgm'] + db_stats['fg3m']
        minus = (db_stats['fga'] - db_stats['fgm']) + (db_stats['fta'] - db_stats['ftm']) \
                + (db_stats['fg3a'] - db_stats['fg3m'] + db_stats['turnovers'])
        db_stats['plus'] = plus
        db_stats['minus'] = minus
        db_stats['score'] = plus - minus
        db_player['stats'].append(db_stats)
        player_collection.update_one({'external_id': external_id}, {'$set': db_player})
        return True
    return False
