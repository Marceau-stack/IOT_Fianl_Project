from django.urls import path
from . import views

urlpatterns = [
    path('temperature', views.temperature_list, name="temperature"),
    path('humidity', views.humidity_list, name="humidity"),
    path('wind', views.wind_list, name="wind"),
    path('history', views.history_list, name="history"),
    path('post_weather', views.post_weather, name='post_weather'),
    path('post_history', views.post_history, name='post_history')
]
