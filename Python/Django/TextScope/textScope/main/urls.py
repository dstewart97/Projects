from django.urls import path
from . import views

urlpatterns = [
    path('', views.tool_view, name='tool_view'),
    path('export/<str:file_type>/', views.export_data, name='export_data'),
]