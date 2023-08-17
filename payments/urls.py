from django.urls import re_path as url
from . import views


urlpatterns = [
    #url(r'^$',views.index, name='index'),
    url(r'^makepayment/$', views.makepayment, name='makepayment'),
    url(r'^paymentStatus/$', views.paymentStatus, name='paymentstatus'),
    url(r'^sucess/$', views.sucess, name='sucess'),
  ]