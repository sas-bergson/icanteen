from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, HTML, Layout, Submit
from django import forms
from django.contrib.auth import get_user_model
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User  
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
  
UserModel = get_user_model()

class FormHelperMixin():
    form_title = 'form_title'
    form_id = 'form_id'
    submit_btn_value = 'submit'
    @property
    def helper(self):
        helper = FormHelper()
        # helper._help_text_inline = True
        helper.form_class = 'icanteenForms'
        helper.form_id = 'id_'+self.form_id
        helper.form_method = 'post'
        helper.form_action = None
        helper.add_input(Submit('submit', self.submit_btn_value, css_class='btn-primary'))
        helper.layout = Layout(
            Div(
                HTML("<h2>"+self.form_title+"</h2>"),
                css_id= 'form-title',
                css_class= 'd-flex form-header-bg-dark justify-content-center',
            ),
        )
        for field in self.fields:
            helper.layout.append(
                Field(field)
        )
        return helper

class AuthenticationForm(FormHelperMixin, auth_forms.AuthenticationForm):
    """ Form that let users to sign in. """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_title = 'Login'
        self.form_id = 'login_form'
        self.submit_btn_value = 'Sign in'


class PasswordChangeForm(FormHelperMixin, auth_forms.PasswordChangeForm):
    """ A form that lets a user change their password. """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_title = 'Change password'
        self.form_id = 'password_change_form'
        self.submit_btn_value = 'Change my password'


class PasswordResetForm(FormHelperMixin, auth_forms.PasswordResetForm):
    """ A form that lets a user reset his/her password. """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_title = 'Send password reset link'
        self.form_id = 'password_reset_form'
        self.submit_btn_value = 'Reset my password'


class SetPasswordForm(FormHelperMixin, auth_forms.SetPasswordForm):
    """ A form that lets a user reset his/her password if he/she forgot the old password. """
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.form_title = 'Change password'
        self.form_id = 'set_password_form'
        self.submit_btn_value = 'Set my new password'


class SignUpForm(FormHelperMixin, auth_forms.UserCreationForm):
    """ A form that lets a user create a new account and sign up. """
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, 
                             required=True,
                             validators=[validators.EmailValidator(message="Invalid Email")],
                             help_text='Required. Provide a valid email address.')   
    class Meta:  
        model = User  
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.form_title = 'Sign Up'
        self.form_id = 'signup_form'
        self.submit_btn_value = 'Sign me up'

    def clean_email(self) -> any:
        """Reject emails that have already been registered."""
        email = self.cleaned_data.get("email")
        if (
            email
            and self._meta.model.objects.filter(email__iexact=email).exists()
        ):
            self._update_errors(
                ValidationError(
                    {
                        "email": self.instance.unique_error_message(
                            self._meta.model, ["email"]
                        )
                    }
                )
            )
        else:
            return email
        
    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ) -> None:
        """ Send a django.core.mail.EmailMultiAlternatives to `to_email`. """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, "text/html")

        email_message.send()

    def save(
        self,
        domain_override=None,
        subject_template_name="registration/account_activation_subject.txt",
        email_template_name="registration/account_activation_email.html",
        use_https=False,
        token_generator=default_token_generator,
        from_email=None,
        request=None,
        html_email_template_name=None,
        extra_email_context=None,
    ) -> None:
        """ Generate a single-use only link for activating the account and mail it to the user. """
        user = super().save(commit=True)       # create a new user model object
        user.is_active = False
        user.is_staff = False
        user.save()
        user_email = self.cleaned_data["email"]
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        
        context = {
            "email": user_email,
            "domain": domain,
            "site_name": site_name,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "user": user,
            "token": token_generator.make_token(user),
            "protocol": "https" if use_https else "http",
            **(extra_email_context or {}),
        }
        self.send_mail(
            subject_template_name,
            email_template_name,
            context,
            from_email,
            user_email,
            html_email_template_name=html_email_template_name,
        )

