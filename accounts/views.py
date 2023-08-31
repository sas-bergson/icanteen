from django.shortcuts import render
from django.template import loader
from django.conf import settings
from django.http import HttpResponse
# Create your views here.

def dashboard(request):
    template = loader.get_template("accounts/index.html")
    context = {'request':request}
    return HttpResponse(template.render(context, request))
