"""icanteen URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from . import views
from django.conf.urls import url




urlpatterns = [
        # urls for the default gallery/
        url(r'^\Z',views.index, name='index'),
        url(r'^wall/$',views.wall, name='wall'),
        url(r'^search/$',views.search, name='search'),
        url(r'^(?P<img_extralarge>[\w/-]+extralargethumb+[.]{1}[a-z]{3,4})/$',views.ExtraLargeThumb, name='extralargethumb'),
        url(r'^(?P<img_large>[\w/-]+largethumb+[.]{1}[a-z]{3,4})/$',views.LargeThumb, name='largethumb'),
        url(r'^(?P<img_medium>[\w/-]+mediumthumb+[.]{1}[a-z]{3,4})/$',views.MediumThumb, name='mediumthumb'),
        url(r'^(?P<img_small>[\w/-]+smallthumb+[.]{1}[a-z]{3,4})/$',views.SmallThumb, name='smallthumb'),
        url(r'^(?P<img_url>[\w/-]+[.]{1}[a-z]{3,4})/$',views.thumbnail, name='thumbnail'),

]

urlpatterns += [
        # urls for product
        url(r'^product/$', views.ProductList, name='product_list'),
        url(r'^(?P<category_slug>[-\w]+)/$', views.ProductList, name='gallery_category_detail'),
        url(r'^product/LargeView/$', views.LargeView, name='largeview'),
        url(r'^product/extraLargeView/$', views.ExtraLargeView, name='extralargeview'),
        url(r'^product/MediumView/$', views.MediumView, name='mediumview'),
        url(r'^product/SmallView/$', views.SmallView, name='smallview'),
        url(r'^product/ListView/$', views.ListView, name='listview'),
        url(r'^product/DetailView/$', views.DetailView, name='detailview'),
        url(r'^product/TileView/$', views.TileView, name='Tileview'),
        url(r'^product/ContentView/$', views.ContentView, name='Contentview'),

        url(r'^product/create/$', views.ProductCreateView.as_view(), name='gallery_product_create'),
        url(r'^product/detail/(?P<slug>\S+)/$', views.ProductDetailView.as_view(), name='gallery_product_detail'),
        url(r'^product/update/(?P<slug>\S+)/$', views.ProductUpdateView.as_view(), name='gallery_product_update'),
        #url(r'^product/$', views.ProductListView.as_view(), name='gallery_product_list'),



]

urlpatterns += [
    # urls for Category
    url(r'^category/$', views.CategoryListView.as_view(), name='gallery_category_list'),
    url(r'^category/create/$', views.CategoryCreateView.as_view(), name='gallery_category_create'),
    #url(r'^category/detail/(?P<category_slug>\S+)/$', views.ProductList, name='gallery_category_detail'),
    url(r'^category/update/(?P<slug>\S+)/$', views.CategoryUpdateView.as_view(), name='gallery_category_update'),
]

