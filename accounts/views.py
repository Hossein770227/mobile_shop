import pytz
import random

from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from datetime import datetime, timedelta

from .forms import LoginForm, UserRegisterForm, VerifyCodeForm
from utils import send_otp_code
from .models import OtpCode, MyUser


class UserRegisterView(View):
    form_class = UserRegisterForm
    def get(self, request):
        form= self.form_class
        return render(request, 'accounts/user_register.html', {'form':form})
    
    def post(self, request):
        form =self.form_class(request.POST)
        if form.is_valid():
            otp = OtpCode.objects.filter(phone_number = form.cleaned_data['phone'])
            if otp.exists():
                messages.error(request, _('we send your code already'))
                return redirect('accounts:verify_code')
            random_code = random.randint(1000, 9999)
            send_otp_code(form.cleaned_data['phone'], random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone'], code=random_code)
            request.session['user_registration_info']={
                'phone_number':form.cleaned_data['phone'],
                'full_name':form.cleaned_data['full_name'],
                'password':form.cleaned_data['password2'],
            }
            messages.success(request, _('we sent you a code'))
            return redirect('accounts:verify_code')
        return render(request, 'accounts/user_register.html', {'form':form})


class UserRegisterCodeView(View):
    form_class = VerifyCodeForm
    template_name = 'accounts/verify_code.html'  
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        user_session = request.session.get('user_registration_info')
        if not user_session:
            messages.error(request, _('Registration information not found.'))
            return redirect('accounts:user_register')  
        
        code_instance = OtpCode.objects.filter(phone_number=user_session['phone_number']).first()

        if not code_instance:
            messages.error(request, _('No code was found for this phone number.'))
            return redirect('accounts:user_register')
        
        form = self.form_class(request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            now = datetime.now(tz=pytz.timezone('Asia/Tehran'))
            expired_time = code_instance.date_time_created + timedelta(minutes=2) 
            
            if now > expired_time:
                code_instance.delete()
                messages.error(request, _('The OTP code has expired.'))
                return redirect('accounts:user_register')  
            
            if cd['code'] == code_instance.code:
                user = MyUser.objects.create_user(user_session['phone_number'], user_session['full_name'], user_session['password'])
                code_instance.delete() 
                messages.success(request, _('You have successfully registered.'))
                login(request, user)  
                return redirect('shop:product_list') 
            else:
                messages.error(request, _('This code is incorrect.'))
                return redirect('accounts:verify_code')  
        
        return redirect('shop:product_list') 


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            user = authenticate(request, username=phone_number, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, _('You have successfully logged in.'))
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('shop:product_list')
            else:
                form.add_error(None, _('phone number or password is incorrect'))
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.method =='POST':
        logout(request)
        messages.error(request, _('you successfully logout'))
        return redirect('shop:product_list')



@login_required
def password_change_view(request):
    if request.method =='POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            messages.success(request, _('your password successfully changed'))
            return redirect('products:product_list')
        return redirect('accounts:change_password')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'accounts/password_change.html',{'form':form})