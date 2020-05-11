from django.urls import path

from . import views

app_name = 'game_manager'
urlpatterns = [
    path('', views.loginView, name='login'),
    path('dashboard/', views.dashboardView, name='dashboard'),
    path('auth/', views.authAction, name='auth'),
    path('games/<int:gameNum>/', views.gameView, name='gameview'),
    path('createBlueprint/', views.createBlueprint, name="createBlueprint"),
    path('gameCreator/<int:num>', views.createGameView, name="createGame"),
]
