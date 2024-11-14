from django.urls import path

from . import views



urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/filter_data/", views.filter_data, name = 'filter_data'),
    path('feedback/', views.feedback_page, name = "feedback"),
    path("feedback/filter_reviews/", views.filter_feedback, name='filter_feedback')
]