from django.urls import path

from . import views



urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/filter_data/", views.filter_data, name = 'filter_data'),
]