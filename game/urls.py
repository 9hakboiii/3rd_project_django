from django.urls import path
from game import views

app_name = 'game'

urlpatterns = [
    path('rps/', views.rps_game, name='rps'),
    path('lotto/', views.lotto_game, name='lotto'),
]
