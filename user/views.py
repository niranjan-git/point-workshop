from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import View
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import FormView, CreateView, UpdateView  
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.utils.decorators import method_decorator
from django.db import transaction

from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from .forms import SignupForm, ForgotPasswordForm, ResetPasswordConfirmForm, OTPVerifyForm, UserLoginForm, form_validation_error
from .models import EmailOTP, User

from django.conf import settings

from .utils import MailUtil, GenerateOTP, RemoveAllSessionKeys, GenerateDefaultPassword
from .decorators import email_session_required, otp_session_required, destroy_session

import json
import math


from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)






def get_client_ip(self):
    request = self.request
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def create_session(self):
    session = ''
    if not self.request.session.exists(self.request.session.session_key):
        # print("session exist")
        self.request.session.create() 
        session = self.request.session.session_key
        self.request.session['session'] = self.request.session.session_key
    else:
        session = self.request.session.session_key
        self.request.session['session'] = session
        # print("session exist else", session)
    return None


@method_decorator(email_session_required, name='dispatch')
class OTPLimitExceededView(generic.TemplateView):
    template_name = "registration/otp_limit_exceeded.html"

    def get_context_data(self, *args, **kwargs):
        context = super(OTPLimitExceededView, self).get_context_data(*args, **kwargs)
        context['message'] = 'OTP send Limit Exceeded'
        
        RemoveAllSessionKeys.remove_sessions(self.request)

        return context



@method_decorator(email_session_required, name='dispatch')
class EmailRegistrationSuccessView(generic.TemplateView):
    template_name = "registration_success.html"

    def get_context_data(self, *args, **kwargs):
        context = super(EmailRegistrationSuccessView, self).get_context_data(*args, **kwargs)
        context['message'] = "Registered Successfully, use your Email and password for login."

        RemoveAllSessionKeys.remove_sessions(self.request)

        return context


@method_decorator(email_session_required, name='dispatch')
class ResetPasswordDoneView(generic.TemplateView):
    template_name = "reset_password_done.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ResetPasswordDoneView, self).get_context_data(*args, **kwargs)
        context['message'] = "Password reset Successfully"

        RemoveAllSessionKeys.remove_sessions(self.request)

        return context


@method_decorator(email_session_required, name='dispatch')
class ActivateUserDoneView(generic.TemplateView):
    template_name = "activate_user_done.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ActivateUserDoneView, self).get_context_data(*args, **kwargs)
        context['message'] = "Account Activated Successfully"

        RemoveAllSessionKeys.remove_sessions(self.request)

        return context




def check_email_exist(email):
    try:
        instance = Email.objects.get(email=email)
        print("in check email exist: ",email)
        if instance:
            print("instance Email id : ", instance)
            return instance.id

    except ObjectDoesNotExist:            
        return None


def check_user_exist(email):
    try:
        instance = User.objects.get(email=email)
        print("in check email exist: ",email)
        if instance:
            print("instance Email id : ", instance)
            return instance.id

    except ObjectDoesNotExist:            
        return None

def is_user_active(email):
    try:
        instance = User.objects.get(email=email, is_active=1)
        print("in is_user_active: ",email)
        if instance:
            print("instance Email id : ", instance)
            return instance.id
        else:
            print("user not active")
            return None
    except ObjectDoesNotExist:
        print("is_user_active, User doesn't exist")            
        return None


def get_otp_count(email_id, session):
    try:
        print("get OTP Count session: ",session)
        ins = EmailOTP.objects.filter(email_id=email_id, session=session).count()
        print("OTP count: ", ins)
        return ins
    except ObjectDoesNotExist:            
        return None


class SignupView(FormView):
    '''
    Signup form view
    '''

    template_name = 'registration.html'
    form_class = SignupForm
    success_url = reverse_lazy('user:verify-otp')


    def form_invalid(self, form):
        print('form invalid')

        return super().form_invalid(form)


    def form_valid(self, form):
        print(form.cleaned_data)
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        confirm = form.cleaned_data["confirm"]
        
        if password != confirm:
            messages.error(self.request, "Password and Confirm Password Must be same")
            return super().form_invalid(form)

        response = dict()

        print("before transaction atomic")

        with transaction.atomic():
            print("within transaction atomic")
            try:
                user = form.save()
                user.refresh_from_db()
                user.set_password(password)
                user.is_active = False
                
                user.save()

                create_session(self)
                self.request.session['email'] = email
                session = self.request.session['session']

                email_id = check_user_exist(email)

                if email_id is not None:
                    otp_ct = get_otp_count(email_id, session)

                    if otp_ct is not None :
                        if otp_ct >= settings.OTP_COUNT_FOR_A_SESSION:
                            messages.error(request, "OTP Resend Limit Exceeded for this session")
                            return super().form_invalid(form)
                        else:
                            data = {
                                'data': email
                            }

                            
                            otp = GenerateOTP.generate_time_based_otp(data) 
                                
                            email_body = f"""<pre>Dear {email} ,
                        The One Time Password (OTP) for your Email Verification for {settings.APP_NAME} is <b>{otp.get('OTP')}</b>

                        This OTP is valid for {math.trunc(int(settings.OTP_EXPIRY_TIME)/60)} minutes or 1 successful attempt, whichever is earlier.

                        Please do not share this One Time Password with anyone.

                    Warm Regards
                    DRDO </pre>"""

                            mail_data={
                                'email_body': email_body,
                                'email_subject': 'Email Verification OTP',
                                'to_email': email
                            }
                        
                        print("OTP to Register: ", otp.get('OTP'))
                        
                        try:
                            eotp = EmailOTP.objects.create(
                                        email_id = email_id,
                                        session = session,
                                        otp = otp.get('OTP')
                                    ) 
                            eotp.save()
                            print("After EmailOTP save")
                            # messages.success(self.request, "OTP sent successfully")

                            #return super().form_valid(form)

                        except:            
                            messages.error(self.request, "Unable to send OTP. Try again Later")
                            return super().form_valid(form)

                        MailUtil.send_mail(mail_data)                   
                
                print("after user save")
            except Exception as e:
                print("Exception in creating user: ",e)
        
        return super().form_valid(form)


@method_decorator(email_session_required, name='dispatch')
class VerifyOTPView(View):
    '''
    Verify Email OTP
    '''

    template_name = 'verify_otp.html'
    form_class = OTPVerifyForm
    success_url = reverse_lazy('user:login')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        if not is_user_active(request.session['email']):
            return render(request, self.template_name, {'form': form})
        else:
            redirect('user:login')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request=request)

        if form.is_valid():
            otp = form.cleaned_data.get('otp')
            ses_email = request.session['email']
            
            
            try:
                email = User.objects.filter(email=ses_email).update(is_active = True)
                
                # RemoveAllSessionKeys.remove_sessions(request)
                
                return HttpResponseRedirect(reverse('user:registration-success'))

            except Exception as e:
                    print(e)
                    print("Email Not found during verifying OTP")      

        return render(request, self.template_name, {'form': form})


class ActivateUserView(FormView):
    '''
    Activate User
    '''
    template_name = 'activate_user.html'
    form_class = ForgotPasswordForm
    success_url = reverse_lazy('user:activate-user-confirm')
    
    def form_invalid(self, form):
        print('form invalid')
        return super().form_invalid(form)

    def form_valid(self, form):
        email = form.cleaned_data['email'].lower()

        print("Email Received at ActivateUserView",email)

        
        email_id = check_user_exist(email)
        print("emailId: ",email_id)
        
        if email_id is not None:
            session = ''
            if not self.request.session.exists(self.request.session.session_key):
                # print("session exist")
                self.request.session.create() 
                session = self.request.session.session_key
                self.request.session['session'] = self.request.session.session_key
            else:
                session = self.request.session.session_key
                self.request.session['session'] = session
                # print("session exist else", session)

            otp_ct = get_otp_count(email_id, session)
            
            if otp_ct is not None:
                if otp_ct >= settings.OTP_COUNT_FOR_A_SESSION:
                    return HttpResponseRedirect(reverse('user:otp-limit-exceeded'))

            try:
                data = {
                    'data': email
                }

                self.request.session['email'] = email

                print("email in session: ",self.request.session['email'])

                otp = GenerateOTP.generate_time_based_otp(data) 
                    
                email_body = f"""<pre>Dear {email} ,
            The One Time Password (OTP) to activate your account for {settings.APP_NAME} is <b>{otp.get('OTP')}</b>

            This OTP is valid for {math.trunc(int(settings.OTP_EXPIRY_TIME)/60)} minutes or 1 successful attempt, whichever is earlier.

            Please do not share this One Time Password with anyone.

        Warm Regards
        DRDO </pre>"""

                mail_data={
                    'email_body': email_body,
                    'email_subject': 'OTP to activate account',
                    'to_email': email
                }
                
                print(otp.get('OTP'))




                eotp = EmailOTP.objects.create(
                            email_id = email_id,
                            session = session,
                            otp = otp.get('OTP')
                        )    
                eotp.save()

                MailUtil.send_mail(mail_data)
            except Exception as e:
                print("Exception during storing OTP in ActivateUserView: ",e)

            MailUtil.send_mail(mail_data)
            return super().form_valid(form)

        else:
            print("Email Not Registered")
            messages.error(self.request, "Email Not Registered")
            return super().form_invalid(form)
        # return super().form_valid(form)



@csrf_exempt
def resend_mail_otp(request):

    response = dict()

    if request.method == "POST":
        print("post")
        if request.session.has_key('email') and request.session.has_key('session'):
            print("email session")
            email = request.session['email']
            session = request.session['session']


            email_id = check_user_exist(email)

            if email_id is not None:
                otp_ct = get_otp_count(email_id, session)

                if otp_ct is not None :
                    if otp_ct >= settings.OTP_COUNT_FOR_A_SESSION:
                        response['message'] = "OTP Resend Limit Exceeded for this session"
                        RemoveAllSessionKeys.remove_sessions(request)
                        return HttpResponse(json.dumps(response), content_type='application/json')
                    else:
                        data = {
                            'data': email
                        }

                        
                        otp = GenerateOTP.generate_time_based_otp(data) 
                            
                        email_body = f"""<pre>Dear {email} ,
                    The One Time Password (OTP) for your Email Verification for {settings.APP_NAME} is <b>{otp.get('OTP')}</b>

                    This OTP is valid for {math.trunc(int(settings.OTP_EXPIRY_TIME)/60)} minutes or 1 successful attempt, whichever is earlier.

                    Please do not share this One Time Password with anyone.

                Warm Regards
                DRDO </pre>"""

                        mail_data={
                            'email_body': email_body,
                            'email_subject': 'Email Verification OTP',
                            'to_email': email
                        }
                    
                    print(otp.get('OTP'))
                    
                    try:
                        eotp = EmailOTP.objects.create(
                                    email_id = email_id,
                                    session = session,
                                    otp = otp.get('OTP')
                                ) 
                        eotp.save()
                        response['message'] = "OTP sent successfully"

                    except:            
                        response['message'] = "Unable to resend OTP. Try again Later"

                    MailUtil.send_mail(mail_data)

                    return HttpResponse(json.dumps(response), content_type='application/json')
                    # return super().form_valid(form)
            
    response['message'] = "Unauthorized Attempt get"
    return HttpResponse(json.dumps(response), content_type='application/json')







# def login_view(request):
#     next = request.GET.get('next')
#     form = UserLoginForm(request.POST or None)
#     if form.is_valid():
#         username = form.cleaned_data.get('username')
#         password = form.cleaned_data.get('password')
#         user = authenticate(username=username, password=password)
#         login(request, user)
#         if next:
#             return redirect(next)
#         return redirect('/')

#     context = {
#         'form': form,
#     }
#     return render(request, "registration/login.html", context)


@method_decorator(destroy_session, name='dispatch')
class LoginView(FormView):
    form_class = UserLoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('participant:submission_list')


    def form_invalid(self, form):
        print('form invalid')

        return super().form_invalid(form)

    def form_valid(self, form):
        # print(form.cleaned_data)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        print("Before Authenticate")
        user = authenticate(username=username, password=password)
        print("user: ",user)
        if user is not None:
            if user.is_active:
                print("active user")
                login(self.request, user)
                return HttpResponseRedirect(reverse('participant:submission_list'))
            else:
                print("Inactive User")
                # return redirect('user:activate-user')
        else:
            print("User doesn't Exist")
            # return HttpResponseRedirect('/user/')
            return super(LoginView, self).form_valid(form)

        # return render(request, "home/index.html")

        return super(LoginView, self).form_valid(form)




class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('user:login')


class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('user:password_change_done')
        else:
            return render(request, 'change_password.html', {'form': form })



class ChangePasswordDoneView(LoginRequiredMixin, generic.TemplateView):
    template_name = "change_password_done.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ChangePasswordDoneView, self).get_context_data(*args, **kwargs)
        context['message'] = 'Your password changed successfully'
        
        RemoveAllSessionKeys.remove_sessions(self.request)

        return context



class ForgotPasswordView(FormView):
    template_name = 'forgot_password.html'
    form_class = ForgotPasswordForm
    success_url = reverse_lazy('user:reset-password-confirm')
    
    def form_invalid(self, form):
        print('form invalid')
        return super().form_invalid(form)

    def form_valid(self, form):
        email = form.cleaned_data['email'].lower()

        print("Email Received at Forgot Password view",email)

        
        email_id = check_user_exist(email)
        print("emailId: ",email_id)
        
        if email_id is not None:
            session = ''
            if not self.request.session.exists(self.request.session.session_key):
                # print("session exist")
                self.request.session.create() 
                session = self.request.session.session_key
                self.request.session['session'] = self.request.session.session_key
            else:
                session = self.request.session.session_key
                self.request.session['session'] = session
                # print("session exist else", session)

            otp_ct = get_otp_count(email_id, session)
            
            if otp_ct is not None:
                if otp_ct >= settings.OTP_COUNT_FOR_A_SESSION:
                    return HttpResponseRedirect(reverse('user:otp-limit-exceeded'))

            try:
                data = {
                    'data': email
                }

                self.request.session['email'] = email

                print("email in session: ",self.request.session['email'])

                otp = GenerateOTP.generate_time_based_otp(data) 
                    
                email_body = f"""<pre>Dear {email} ,
            The One Time Password (OTP) for Forgot Password for {settings.APP_NAME} is <b>{otp.get('OTP')}</b>

            This OTP is valid for {math.trunc(int(settings.OTP_EXPIRY_TIME)/60)} minutes or 1 successful attempt, whichever is earlier.

            Please do not share this One Time Password with anyone.

        Warm Regards
        DRDO </pre>"""

                mail_data={
                    'email_body': email_body,
                    'email_subject': 'Reset Password OTP',
                    'to_email': email
                }
                
                print(otp.get('OTP'))




                eotp = EmailOTP.objects.create(
                            email_id = email_id,
                            session = session,
                            otp = otp.get('OTP')
                        )    
                eotp.save()

                MailUtil.send_mail(mail_data)
            except Exception as e:
                print("Exception during storing OTP in forgot password: ",e)

            MailUtil.send_mail(mail_data)
            return super().form_valid(form)

        else:
            print("Email Not Registered")
            messages.error(self.request, "Email Not Registered")
            return super().form_invalid(form)
        # return super().form_valid(form)


@method_decorator(email_session_required, name='dispatch')
class ResetPasswordConfirmView(FormView):
    template_name = 'reset_password_confirm.html'
    form_class = ResetPasswordConfirmForm
    success_url = reverse_lazy('user:reset-password-done')
    
    def form_invalid(self, form):
        print('form invalid')
        return super().form_invalid(form)

    def form_valid(self, form):
        # print(self.request.session['email'])
        otp = form.cleaned_data.get('otp')
        password = form.cleaned_data["password"]
        confirm = form.cleaned_data["confirm"]

        # print(password,"  ",confirm)

        if password != confirm:
            messages.error(self.request, "Password and Confirm Password Must be same")
            return super().form_invalid(form)
        
        ses_email = self.request.session['email']

        data = {
            'email': ses_email,
            'otp': otp
            
        }
        if GenerateOTP.verify_time_based_top(data):
            print('otp true')
            self.request.session['otp'] = True
        else:
            messages.error(self.request, "OTP Invalid/Expired")
            print('validation error OTP')
        
        try:
            user = User.objects.get(email=ses_email)
            if user is not None:
                user.set_password(password)
                user.save()
                print("after user save")
            else:
                messages.error(self.request, "User does not Exist")
                return super().form_invalid(form)
        except Exception as e:
            print("Exception in Resetting user password: ",e)
            messages.error(self.request, "Some Error occured in resetting password, Try again later!")
            return super().form_invalid(form)

        return super().form_valid(form)


@method_decorator(email_session_required, name='dispatch')
class ActivateUserConfirmView(FormView):
    template_name = 'activate_user_confirm.html'
    form_class = OTPVerifyForm
    success_url = reverse_lazy('user:activate_user_done')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        if not is_user_active(request.session['email']):
            return render(request, self.template_name, {'form': form})
        else:
            redirect('user:login')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request=request)

        if form.is_valid():
            otp = form.cleaned_data.get('otp')
            ses_email = request.session['email']
            
            
            try:
                email = User.objects.filter(email=ses_email).update(is_active = True)
                
                # RemoveAllSessionKeys.remove_sessions(request)
                
                return HttpResponseRedirect(reverse('user:activate-user-done'))

            except Exception as e:
                    print(e)
                    print("Email Not found during Activating Account")      

        return render(request, self.template_name, {'form': form})

    
