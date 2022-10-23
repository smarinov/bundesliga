from django.urls import path

from bundes.views import landing_page, upcoming_matches, win_loss_ratio, team_details, current_season_matches, search

urlpatterns = [
    path('', landing_page, name='homepage'),
    path('current-season/', current_season_matches, name='current season matches'),
    path('upcoming/', upcoming_matches, name='upcoming matches'),
    path('win-loss-ratio/', win_loss_ratio, name='win loss ratio'),
    path('team-details/<str:name>', team_details, name='team details'),
    path('search/', search, name='search'),
]
