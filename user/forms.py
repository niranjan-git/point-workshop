from django.db import models
from django import forms
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.conf import settings

from captcha.fields import CaptchaField

from .models import User
from .utils import GenerateOTP

from django.contrib.auth import (
    authenticate,
    get_user_model

)

class SignupForm(forms.ModelForm):
    password = forms.CharField(max_length=settings.PASSWORD_MAX_LEN, required=True, widget=forms.PasswordInput())
    confirm = forms.CharField(max_length=settings.PASSWORD_MAX_LEN, required=True, widget=forms.PasswordInput())
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ('email', 'password', 'confirm')

    # def clean_password(self):
    #     print("in clean")
    #     # cleaned_data = super(SignupForm, self).clean()
    #     password = self.cleaned_data.get("password")
    #     confirm_password = self.cleaned_data.get("confirm")

    #     if password != confirm_password:
    #         raise forms.ValidationError(
    #             "Password and Confirm Password Must be same"
    #         )
            
    #     return password


class ForgotPasswordForm(forms.Form):
    email = forms.CharField()
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
       self.request = kwargs.pop("request", None)
       super(ForgotPasswordForm, self).__init__(*args, **kwargs)


class ResetPasswordConfirmForm(forms.Form):
    otp = forms.CharField(max_length=6)
    password = forms.CharField(max_length=settings.PASSWORD_MAX_LEN, required=True, widget=forms.PasswordInput())
    confirm = forms.CharField(max_length=settings.PASSWORD_MAX_LEN, required=True, widget=forms.PasswordInput())
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
       self.request = kwargs.pop("request", None)
       super(ResetPasswordConfirmForm, self).__init__(*args, **kwargs)

    # def clean_otp(self):
    #     print("in clean")
    #     otp = self.cleaned_data['otp']
    #     ses_email = self.request.session['email']

    #     print(otp," ",ses_email)

    #     data = {
    #         'email': ses_email,
    #         'otp': otp
            
    #     }
    #     if GenerateOTP.verify_time_based_top(data):
    #         print('otp true')
    #         self.request.session['otp'] = True
    #         return otp
    #     print('validation error OTP')
    #     raise ValidationError("OTP Invalid/Expired")

    #     return otp

    
    





class OTPVerifyForm(forms.Form):
    otp = forms.CharField(max_length=6)

    def __init__(self, *args, **kwargs):
       self.request = kwargs.pop("request", None)
       super(OTPVerifyForm, self).__init__(*args, **kwargs)


    def clean_otp(self):
        print("in clean")
        otp = self.cleaned_data['otp']
        ses_email = self.request.session['email']

        print(otp," ",ses_email)

        data = {
            'email': ses_email,
            'otp': otp
            
        }
        if GenerateOTP.verify_time_based_top(data):
            print('otp true')
            self.request.session['otp'] = True
            return otp
        print('validation error OTP')
        raise ValidationError("OTP Invalid/Expired")

        return otp




class UserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class UserLoginForm(forms.Form):
    username = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = CaptchaField()

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            print("In form clean inside if")
            user = authenticate(username=username, password=password)
            print("user: ",user)
            if not user:
                print("Username or password invalid")
                raise forms.ValidationError("Username or password invalid")
            if not user.is_active:
                print("User not Active")
                activation_link = "Account inactive. click <a href='{0}'>here</a> to activate.".format(reverse_lazy('user:activate-user'))
                raise forms.ValidationError(mark_safe(activation_link))
        return super(UserLoginForm, self).clean(*args, **kwargs)



def form_validation_error(form):
    """
    Form Validation Error
    If any error happened in your form, this function returns the error message.
    """
    msg = ""
    for field in form:
        for error in field.errors:
            msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
    return msg