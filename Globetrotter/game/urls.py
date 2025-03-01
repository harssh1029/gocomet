from django.urls import path
from .views import game_home, get_random_destination, load_data



urlpatterns = [
    path('', game_home, name='game_home'),
    path('random/', get_random_destination, name='random_destination'),
    path('load-data/', load_data, name='load_data'),
]
