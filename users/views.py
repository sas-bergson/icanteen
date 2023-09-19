from django.contrib.auth import get_user_model, \
                                login as auth_login, \
                                views as auth_views
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import  ImproperlyConfigured, \
                                    ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import CreateView
from django.views.generic.base import TemplateView

from .forms import(
    SignUpForm,
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)

# Create your views here.

UserModel = get_user_model()

class DashboardView(auth_views.RedirectURLMixin, TemplateView):
    template_name = "users/index.html"

class LoginView(auth_views.LoginView):
    """ Display the login form and handle the login action."""
    form_class = AuthenticationForm
    template_name = "auth/login.html"

class LogoutView(auth_views.LogoutView):
    """ Display the log out page."""
    template_name = "auth/logged_out.html"

class PasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    """ Display the Password Change Done page and invite the user to logout then login."""
    template_name = "auth/password_change_done.html"

class PasswordChangeView(auth_views.PasswordChangeView):
    """ Display the Password Change Form """
    form_class = PasswordChangeForm
    template_name = "auth/password_change_form.html"
    success_url = reverse_lazy('users:password_change_done')

class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    """ Display the Password Reset Done page and invite the user open email and click on the reset link."""
    template_name = "auth/password_reset_sent.html"

class PasswordResetView(auth_views.PasswordResetView):
    """ Display the Password Reset Form."""
    form_class = PasswordResetForm
    template_name = "auth/password_reset_form.html"
    success_url = reverse_lazy('users:password_reset_link_sent')
    email_template_name = "auth/password_reset_email.html"
    html_email_template_name = "auth/password_reset_email.html"
    subject_template_name = "auth/password_reset_subject.txt"

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    """ Display the Password Reset Form."""
    form_class = SetPasswordForm
    template_name = "auth/password_reset_confirm.html"
    success_url = reverse_lazy('users:password_reset_complete')

class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    """ Display the Password Reset Complete page and invite the user to login with the new password."""
    template_name = "auth/password_reset_complete.html"

# def signup(request):  
#     if request.method == 'POST':  
#         form = SignUpForm(request.POST)  
#         if form.is_valid():  
#             # save form in the memory not in database  
#             user = form.save(commit=False)  
#             user.is_active = False  
#             user.save()  
#             # to get the domain of the current site  
#             current_site = get_current_site(request)  
#             mail_subject = 'Activation link has been sent to your email id'  
#             message = render_to_string('acc_active_email.html', {  
#                 'user': user,  
#                 'domain': current_site.domain,  
#                 'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
#                 'token':account_activation_token.make_token(user),  
#             })  
#             to_email = form.cleaned_data.get('email')  
#             email = EmailMessage(  
#                         mail_subject, message, to=[to_email]  
#             )  
#             email.send()  
#             return HttpResponse('Please confirm your email address to complete the registration')  
#     else:  
#         form = SignUpForm()  
#     return render(request, 'signup.html', {'form': form})


# Class-based signup views
# - SignupView creates a new user then sends activation mail
# - SignupDoneView shows a success message for the above
# - SignupActivationView checks the link the user clicked and activates the new account
# - SignupCompleteView shows a success message for the above

class SignupContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {"title": self.title, "subtitle": None, **(self.extra_context or {})}
        )
        return context

class SignUpView(CreateView):
    email_template_name = "registration/account_activation_email.html"
    extra_email_context = None
    form_class = SignUpForm
    from_email = None
    html_email_template_name = "registration/account_activation_email.html"
    subject_template_name="registration/account_activation_subject.txt"
    success_url = reverse_lazy("users:account_signup_activation_sent")
    template_name = "registration/signup_form.html"
    title = _("Sign Up")
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        opts = {
            "use_https": self.request.is_secure(),
            "token_generator": self.token_generator,
            "from_email": self.from_email,
            "email_template_name": self.email_template_name,
            "subject_template_name": self.subject_template_name,
            "request": self.request,
            "html_email_template_name": self.html_email_template_name,
            "extra_email_context": self.extra_email_context,
        }
        form.save(**opts)
        return HttpResponseRedirect(self.success_url)
    
class SignUpDoneView(SignupContextMixin, TemplateView):
    template_name = "registration/signup_activation_sent.html"
    title = _("Signup Activation link sent")

INTERNAL_RESET_SESSION_TOKEN = "_account_activation_token"

class SignUpActivationView(SignupContextMixin, TemplateView):
    account_activation_url_token = "account-activation"
    success_url = reverse_lazy("users:signup_complete")
    template_name = "registration/signup_account_activation.html"
    title = _("Signup Account Activation")
    token_generator = default_token_generator

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        if "uidb64" not in kwargs or "token" not in kwargs:
            raise ImproperlyConfigured(
                "The URL path must contain 'uidb64' and 'token' parameters."
            )

        self.validlink = False
        self.user = self.get_user(kwargs["uidb64"])

        if self.user is not None:
            token = kwargs["token"]
            if token == self.account_activation_url_token:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the account actvation successful page.
                    self.validlink = True
                    del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # Signup Form URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(
                        token, self.account_activation_url_token
                    )
                    return HttpResponseRedirect(redirect_url)

        # Display the "Account activation unsuccessful" page.
        return self.render_to_response(self.get_context_data())

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
            user.is_active = True
            user.save()
        except (
            TypeError,
            ValueError,
            OverflowError,
            UserModel.DoesNotExist,
            ValidationError,
        ):
            user = None
        return user

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs["user"] = self.user
    #     return kwargs

    # def form_valid(self, form):
    #     user = form.save()
    #     del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
    #     if self.post_reset_login:
    #         auth_login(self.request, user, self.post_reset_login_backend)
    #     return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context["validlink"] = True
        else:
            context.update(
                {
                    # "form": None,
                    "title": _("Signup Account Activation unsuccessful"),
                    "validlink": False,
                }
            )
        return context