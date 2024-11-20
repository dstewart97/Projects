from django.urls import path
from . import views

urlpatterns = [
    path('', views.tool_view, name='tool_view'),
    path('edit-topic/<int:topic_id>/', views.edit_topic, name='edit_topic'),
]