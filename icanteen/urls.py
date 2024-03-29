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
from django.conf import settings
from django.conf.urls import include
from django.urls import re_path as url
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    url(r'^\Z',         include('home.urls')),
    url(r'^admin/',     admin.site.urls),
    url(r'^polls/',     include('polls.urls')),
    url(r'^slideshow/', include('slideshow.urls')),
    url(r'^cart/',      include('cart.urls')),
    url(r'^orders/',    include('orders.urls')),
    url(r'^gallery/',   include('gallery.urls')),
    url(r'^payment/',   include('payments.urls')),
    url(r'^maps/',      include('maps.urls')),
    url(r'^users/',   include('users.urls')),
    url(r'^__debug__/',   include('debug_toolbar.urls')),
  ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



