from django.shortcuts import render, redirect
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

        return all_teams

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


def landing_page(request):
    return render(request, 'home.html')


def upcoming_matches(request):
    next_day_matches = RequestHandler.get_upcoming_matches()

    for x in next_day_matches:
        x['MatchDateTime'] = x['MatchDateTime'].replace('T', ' ')

    context = {'next_day_matches': next_day_matches,
               'tomorrow_date': TOMORROW, }
    return render(request, 'upcoming.html', context)


def current_season_matches(request):
    matches_data = RequestHandler.get_current_season_matches()

    context = {
        'matches_data': matches_data,
        'current_year': CURRENT_YEAR,
    }
    return render(request, 'current_season.html', context)


def win_loss_ratio(request):
    all_teams = RequestHandler.get_win_loss_ratio()

    context = {'all_teams': all_teams,
               'current_year': CURRENT_YEAR, }
    return render(request, 'win_loss_ratio.html', context)


def team_details(request, name):
    team_exists = RequestHandler.check_if_team_exists(name)

    if not team_exists:
        return redirect('current season matches')

    current_team_next_day_matches = RequestHandler.get_current_team_upcoming_matches(name)
    current_team_all_matches_season = RequestHandler.get_all_matches_current_team_for_the_season(name)
    current_team_ratio = RequestHandler.get_current_team_win_loss_ratio(name)
    current_team_icon = RequestHandler.get_current_team_icon(name)

    context = {'team_name': name,
               'upcoming_matches': current_team_next_day_matches,
               'all_matches': current_team_all_matches_season,
               'current_team_ratio': current_team_ratio,
               'current_team_icon': current_team_icon,
               }

    return render(request, 'team_details.html', context)


def search(request):
    search_team = request.GET.get('search').strip()
    correct_name = RequestHandler.check_if_team_exists(search_team)
    if correct_name:
        search_team = correct_name[0]['TeamName']

    if not search_team:
        return redirect('current season matches')

    return team_details(request, search_team)
