from django.urls import re_path as url
from . import views

app_name = 'cart'

urlpatterns = [
    url(r'^$', views.cart_detail, name='details'),   #url to display the cart detail page
    url(r'^add/(?P<product_id>\d+)/$', views.cart_add, name='add'), #definition of url to add items to cart
    url(r'^remove/(?P<product_id>\d+)/$', views.cart_remove, name='remove'), # the url to remove product from cart

]
    #url(r'^$', views.cart_detail, name='cart_detail'),   #url to display the cart detail page
    #url(r'^add/(?P<product_id>\d+)/$', views.cart_add, name='cart_add'), #definition of url to add items to cart

