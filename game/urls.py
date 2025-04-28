from django.urls import path
from game import views

app_name = 'game'

urlpatterns = [
    path('rps/', views.rsp_game, name='rsp_game'),
    path('lotto/', views.lotto_game, name='lotto_game'),
]
