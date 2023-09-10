from django.conf.urls import include
from django.urls import re_path as url
from users import views

app_name = 'users'

urlpatterns = [
    # url(r"^", include("django.contrib.auth.urls")),
    # url(r'^dashboard/', views.dashboard, name='dashboard'),
    url("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    url("login/", views.LoginView.as_view(), name="login"),
    url("logout/", views.LogoutView.as_view(), name="logout"),
    url("password_change/", views.PasswordChangeView.as_view(), name="password_change"),
    url("password_change/done/",views.PasswordChangeDoneView.as_view(),name="password_change_done"),
    url("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
    url("password_reset/done/",views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    url("reset/(?P<uidb64>[\w-]+)/(?P<token>[\w-]+)/",views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    url("reset/done/",views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
]
