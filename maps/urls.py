from django.conf.urls import url
from . import views

app_name = 'maps'

urlpatterns = [
    url(r'^Customer_details/$',views.Customer_details, name='Customer_details'),
     url(r'^searchmenu/$',views.searchmenu, name='Customer_details'),

]
