from django.conf.urls import include
from django.urls import re_path as url
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

from users import views

app_name = 'users'

# When designing custom user authentication views, you should:
#     redefine the django.contrib.auth.urls especially the PasswordResetView
#     Define the PasswordChangeDoneView before the PasswordChangeView (if not you will get a strange url reloading error)
#     Define the PasswordResetDoneView before the PasswordResetView (if not you will get a strange url reloading error)

urlpatterns = [
    # url(r"^", include("django.contrib.auth.urls")),
    url("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    url("login/", views.LoginView.as_view(), name="login"),
    url("logout/", views.LogoutView.as_view(), name="logout"),
    url("password_change/done/",views.PasswordChangeDoneView.as_view(),name="password_change_done"),
    url("password_change/", views.PasswordChangeView.as_view(), name="password_change"),
    url("password_reset/done/",views.PasswordResetDoneView.as_view(),name="password_reset_link_sent"),
    url("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
    url("reset/(?P<uidb64>[\w-]+)/(?P<token>[\w-]+)/",views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    url("reset/done/",views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
    url("signup/done/", views.SignUpDoneView.as_view(), name="account_signup_activation_sent"),
    url("signup/", views.SignUpView.as_view(), name="account_signup"),
    url("signup_activation/(?P<uidb64>[\w-]+)/(?P<token>[\w-]+)/", views.SignUpActivationView.as_view(), name="account_activation_confirm"),
]
