import requests
from datetime import date, timedelta

BASE_URL = 'https://www.openligadb.de/api/'

TODAY = date.today()
TOMORROW = date.today() + timedelta(days=1)
CURRENT_YEAR = date.today().year


class RequestHandler:

    @staticmethod
    def get_upcoming_matches():
        response = requests.get(BASE_URL + f'getmatchdata/bl1/{TODAY.year}')
        data = response.json()
        next_day_matches = [match for match in data if
                            f'{TOMORROW.year}-{TOMORROW.month}-{TOMORROW.day}' in match['MatchDateTime']]
        return next_day_matches

    @staticmethod
    def get_current_season_matches():
        response = requests.get(BASE_URL + f'getmatchdata/bl1/{TODAY.year}')
        data = response.json()
        all_matches = data
        matches_data = []
        for match in all_matches:
            to_append_data = {
                'match_id': match['MatchID'],
                'home_team': match['Team1']['TeamName'],
                'away_team': match['Team2']['TeamName'],
                'match_date_time': match['MatchDateTime'].replace('T', ' '),
                'match_is_finished': match['MatchIsFinished'],
                'first_half_result': f"{match['MatchResults'][1]['PointsTeam1']} : {match['MatchResults'][1]['PointsTeam2']}" if
                match['MatchIsFinished'] else '- : -',
                'second_half_result': f"{match['MatchResults'][0]['PointsTeam1']} : {match['MatchResults'][0]['PointsTeam2']}" if
                match['MatchIsFinished'] else '- : -',
            }
            matches_data.append(to_append_data)
        return matches_data

    @staticmethod
    def get_win_loss_ratio():
        response_teams = requests.get(BASE_URL + f'getavailableteams/bl1/{TODAY.year}')
        data_teams = response_teams.json()
        response_results = requests.get(BASE_URL + f'getmatchdata/bl1/{TODAY.year}')
        data_results = response_results.json()
        all_teams = {}
        for team in data_teams:
            all_teams[f'{team["TeamName"]}'] = {'wins': 0, 'losses': 0, 'draws': 0}
        for result in data_results:
            if result['MatchIsFinished']:
                if result['MatchResults'][0]['PointsTeam1'] > result['MatchResults'][0]['PointsTeam2']:
                    all_teams[f"{result['Team1']['TeamName']}"]['wins'] += 1
                    all_teams[f"{result['Team2']['TeamName']}"]['losses'] += 1
                elif result['MatchResults'][0]['PointsTeam1'] == result['MatchResults'][0]['PointsTeam2']:
                    all_teams[f"{result['Team1']['TeamName']}"]['draws'] += 1
                    all_teams[f"{result['Team2']['TeamName']}"]['draws'] += 1
                elif result['MatchResults'][0]['PointsTeam1'] < result['MatchResults'][0]['PointsTeam2']:
                    all_teams[f"{result['Team1']['TeamName']}"]['losses'] += 1
                    all_teams[f"{result['Team2']['TeamName']}"]['wins'] += 1

        for team in all_teams:
            winning_percentage = f"{((all_teams[team]['wins'] + (all_teams[team]['draws'] * 0.5)) / sum([all_teams[team]['wins'], all_teams[team]['draws'], all_teams[team]['losses']])) * 100:.2f}%"
            all_teams[team]['winning_percentage'] = winning_percentage

        sorted_all_teams_by_winning_percentage = sorted(all_teams.items(), key=lambda x: x[1]['winning_percentage'],
                                                        reverse=True)

        return dict(sorted_all_teams_by_winning_percentage)

    @staticmethod
    def check_if_team_exists(name):
        response = requests.get(BASE_URL + f'getavailableteams/bl1/{TODAY.year}')
        data = response.json()
        team = [team for team in data if f'{name.lower()}' == team['TeamName'].lower()]
        if team:
            return team

    @staticmethod
    def get_current_team_upcoming_matches(name):
        response = requests.get(BASE_URL + f'getmatchdata/bl1/{TODAY.year}')
        data = response.json()
        next_day_matches = [match for match in data if
                            f'{TOMORROW.year}-{TOMORROW.month}-{TOMORROW.day}' in match['MatchDateTime']]
        current_team_next_day_matches = [match for match in next_day_matches if name in
                                         match['Team1']['TeamName'] or name in match['Team2']['TeamName']]
        return current_team_next_day_matches

    @staticmethod
    def get_all_matches_current_team_for_the_season(name):
        response = requests.get(BASE_URL + f'getmatchdata/bl1/{TODAY.year}')
        data = response.json()
        current_team_all_matches = []
        for match in data:
            if name in match['Team1']['TeamName'] or name in match['Team2']['TeamName']:
                match_data = {
                    'match_id': match['MatchID'],
                    'home_team': match['Team1']['TeamName'],
                    'away_team': match['Team2']['TeamName'],
                    'match_date_time': match['MatchDateTime'].replace('T', ' '),
                    'first_half_result': f"{match['MatchResults'][1]['PointsTeam1']} : {match['MatchResults'][1]['PointsTeam2']}" if
                    match['MatchIsFinished'] else '- : -',
                    'second_half_result': f"{match['MatchResults'][0]['PointsTeam1']} : {match['MatchResults'][0]['PointsTeam2']}" if
                    match['MatchIsFinished'] else '- : -', }

                current_team_all_matches.append(match_data)

        return current_team_all_matches

    @staticmethod
    def get_current_team_win_loss_ratio(name):
        response = requests.get(BASE_URL + f'getmatchdata/bl1/{TODAY.year}')
        data = response.json()
        current_team_ratio = {'wins': 0,
                              'losses': 0,
                              'draws': 0, }
        for match in data:
            if match['MatchIsFinished']:
                if name == match['Team1']['TeamName']:
                    if match['MatchResults'][0]['PointsTeam1'] > match['MatchResults'][0]['PointsTeam2']:
                        current_team_ratio['wins'] += 1
                    elif match['MatchResults'][0]['PointsTeam1'] < match['MatchResults'][0]['PointsTeam2']:
                        current_team_ratio['losses'] += 1
                    else:
                        current_team_ratio['draws'] += 1
                elif name == match['Team2']['TeamName']:
                    if match['MatchResults'][0]['PointsTeam2'] > match['MatchResults'][0]['PointsTeam1']:
                        current_team_ratio['wins'] += 1
                    elif match['MatchResults'][0]['PointsTeam2'] < match['MatchResults'][0]['PointsTeam1']:
                        current_team_ratio['losses'] += 1
                    else:
                        current_team_ratio['draws'] += 1
        return current_team_ratio

    @staticmethod
    def get_current_team_icon(name):
        response = requests.get(BASE_URL + f'getavailableteams/bl1/{TODAY.year}')
        data = response.json()
        team = [team for team in data if
                f'{name}' == team['TeamName']]
        return team[0]['TeamIconUrl']
