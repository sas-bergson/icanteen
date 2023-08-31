from django.urls import re_path as url
from . import views

app_name = 'payments'

urlpatterns = [
    #url(r'^$',views.index, name='index'),
    url(r'^makepayment/$', views.makepayment, name='makepayment'),
    url(r'^paymentStatus/$', views.paymentStatus, name='status'),
    url(r'^sucess/$', views.success, name='success'),
  ]