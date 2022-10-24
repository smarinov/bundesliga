from django.shortcuts import render, redirect
from bundes.req_handler import RequestHandler
from datetime import date, timedelta

TODAY = date.today()
TOMORROW = date.today() + timedelta(days=1)
CURRENT_YEAR = date.today().year


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
