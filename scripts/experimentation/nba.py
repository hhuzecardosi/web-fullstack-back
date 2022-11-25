import json

from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster, scoreboardv2
import pandas
from nba_api.live.nba.endpoints import playbyplay
from nba_api.live.nba.endpoints import boxscore

from nba_api.stats.endpoints import leagueseasonmatchups


# Today's Score Board
# games = scoreboard.ScoreBoard().get_json()
# print(games)

# json
# json = games.get_json()
# print(json)

# dictionary
# games.get_dict()

# teams = teams.get_teams()
# print(teams)

# play = playbyplay.PlayByPlay('0022200081')
# print(play.get_json())

scores = boxscore.BoxScore('0022200260')
print(scores.get_json())

# scores = boxscore.BoxScore('0022200755')
# print(scores.get_json())

# team = commonteamroster.CommonTeamRoster('1610612737')
# print(team.get_dict())

# schedule = leagueseasonmatchups.LeagueSeasonMatchups(league_id='00', season='2022-23',
# season_type_playoffs='Regular Season', per_mode_simple='Totals')
# print(schedule.get_json())

#games = scoreboardv2.ScoreboardV2(game_date='2022-10-18').get_normalized_json()
# df = games.get_normalized_dict()
# print(df)
#print(games)

# game = scoreboard.Scoreboard(league_id='00', day_offset='0', game_date='2022-10-20')
# print(game.get_normalized_json())


roster = commonteamroster.CommonTeamRoster(1610612738).get_dict()