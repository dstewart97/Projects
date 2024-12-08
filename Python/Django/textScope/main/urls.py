from django.urls import path
from . import views

urlpatterns = [
    path('', views.tool_view, name='tool_view'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('contact_view/', views.contact_view, name='contact_view'),
    path('export/<str:file_type>/', views.export_data, name='export_data'),
    path('add_temp_topic/', views.add_temp_topic, name='add_temp_topic'),
]