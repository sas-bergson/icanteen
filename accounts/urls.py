from django.urls import re_path as url
from . import views

app_name = 'accounts'

urlpatterns = [
    url(r'^dashboard/', views.dashboard, name='dashboard'),
]
