from django.conf.urls import include
from django.urls import re_path as url
from users import views
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

app_name = 'users'

# When designing custom user authentication views, you should:
#     redefine the django.contrib.auth.urls especially the PasswordResetView
#     Define the PasswordChangeDoneView before the PasswordChangeView (if not you will get a strange url reloading error)
#     Define the PasswordResetDoneView before the PasswordResetView (if not you will get a strange url reloading error)

urlpatterns = [
    # url(r"^", include("django.contrib.auth.urls")),
    url("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    url("login/", auth_views.LoginView.as_view(template_name= 'auth/login.html'), name="login"),
    url("logout/", auth_views.LogoutView.as_view(template_name= 'auth/logged_out.html'), name="logout"),
    url("password_change/done/",auth_views.PasswordChangeDoneView.as_view(template_name = 'auth/password_change_done.html'),name="password_change_done"),
    url("password_change/", auth_views.PasswordChangeView.as_view(template_name = 'auth/password_change_form.html', success_url = reverse_lazy('users:password_change_done')), name="password_change"),
    url("password_reset/done/",auth_views.PasswordResetDoneView.as_view(template_name = 'auth/password_reset_sent.html'),name="password_reset_done"),
    url("password_reset/", auth_views.PasswordResetView.as_view(template_name = 'auth/password_reset_form.html', success_url = reverse_lazy('users:password_reset_done'), html_email_template_name = 'registration/password_reset_email.html'), name="password_reset"),
    url("reset/(?P<uidb64>[\w-]+)/(?P<token>[\w-]+)/",auth_views.PasswordResetConfirmView.as_view(template_name = 'registration/password_reset_confirm.html', success_url = reverse_lazy('users:password_reset_complete')),name="password_reset_confirm"),
    url("reset/done/",auth_views.PasswordResetCompleteView.as_view(template_name = 'registration/password_reset_complete.html'),name="password_reset_complete"),
]
