from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import (
     SignupView, resend_mail_otp, VerifyOTPView, ActivateUserView, ActivateUserConfirmView, ActivateUserDoneView, OTPLimitExceededView, EmailRegistrationSuccessView, LoginView, ChangePasswordView, ChangePasswordDoneView, ForgotPasswordView, ResetPasswordConfirmView, ResetPasswordDoneView, LogoutView
)


app_name = 'user'


urlpatterns = [
    path('register/', SignupView.as_view(), name='send-email-otp'),
    path('resend-email-otp/', resend_mail_otp, name='resend-email-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('activate-user/', ActivateUserView.as_view(), name='activate-user'),
    path('activate-user-confirm/', ActivateUserConfirmView.as_view(), name='activate-user-confirm'),
    path('activate_user_done/', ActivateUserDoneView.as_view(), name='activate-user-done'),
    path('otp_limit_exceeded/', OTPLimitExceededView.as_view(), name='otp-limit-exceeded'),
    path('registration_success/', EmailRegistrationSuccessView.as_view(), name='registration-success'),

    path('', LoginView.as_view(), name='login'),
    path('password_change/', ChangePasswordView.as_view(), name='password_change'),
    path('password_change_done/', ChangePasswordDoneView.as_view(), name='password_change_done'),
    path('forgot_password/', ForgotPasswordView.as_view(), name='password_forgot'),
    path('reset_password_confirm/', ResetPasswordConfirmView.as_view(), name='reset-password-confirm'),
    path('reset_password_done/', ResetPasswordDoneView.as_view(), name='reset-password-done'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
]