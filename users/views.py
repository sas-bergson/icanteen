from django.shortcuts import render
from django.template import loader
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.contrib.auth.views import (
    RedirectURLMixin,
    LoginView,
    LogoutView,
    PasswordContextMixin,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordChangeView,
    PasswordChangeDoneView,
)
# Create your views here.

# def dashboard(request):
#     template = loader.get_template("users/index.html")
#     context = {'request':request}
#     return HttpResponse(template.render(context, request))

class DashboardView(RedirectURLMixin, TemplateView):
    template_name = "users/index.html"
    extra_context = None

class LoginView(LoginView):
    template_name = "registration/login.html"

class PasswordResetView(PasswordResetView):
    html_email_template_name = "registration/password_reset_email.html"
    success_url = reverse_lazy("users:password_reset_done")
    template_name = "registration/password_reset_form.html"

class PasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy("users:password_reset_complete")
    template_name = "registration/password_reset_confirm.html"

class PasswordResetDoneView(PasswordResetDoneView):
    template_name = "registration/reset_done.html"

class PasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy("users:password_change_done")
