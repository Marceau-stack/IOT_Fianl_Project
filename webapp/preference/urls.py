from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_preference, name="preference"),
    path('update', views.update_preference, name="preference_update")
]
