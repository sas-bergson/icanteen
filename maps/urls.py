from django.urls import re_path as url
from . import views

app_name = 'maps'

urlpatterns = [
    url(r'^Customer_details/$',views.Customer_details, name='customer_details'),
     url(r'^searchmenu/$',views.searchmenu, name='search_menu'),

]
