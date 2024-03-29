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

from django.urls import re_path as url
from . import views

app_name = 'polls'

urlpatterns = [
        #polls/
        url(r'^$',views.index, name='index'),
        #polls/<question_id>
        url(r'^(?P<question_id>[0-9]+)/$',views.detail, name='detail'),
        #polls/<question_id>/results
        url(r'^(?P<question_id>[0-9]+)/results/$',views.results, name='results'),
        #polls/<question_id/votes>
        url(r'^(?P<question_id>[0-9]+)/vote/$',views.vote, name='vote'),
]
