from django.shortcuts import render
from django.template import loader
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.contrib.auth.views import RedirectURLMixin

# Create your views here.

class DashboardView(RedirectURLMixin, TemplateView):
    template_name = "users/index.html"
    extra_context = None
