from django.conf.urls import url
#from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    url(r'^create/$', views.order_create, name='order_create'), #the url for order_create in the views.py file
    #path('admin/order/<int:order_id>pdf/', views.admin_order_pdf, name='admin_order_pdf'),
    url(r'^pdf/(?P<order_id>\d+)/$', views.admin_order_detail, name='admin_order_detail'),
    url(r'^pdf/(?P<order_id>\d+)/$', views.admin_order_pdf, name='admin_order_pdf'),
]
#url(r'^add/(?P<product_id>\d+)/$', views.cart_add, name='cart_add'),
