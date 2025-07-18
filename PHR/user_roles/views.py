from django.shortcuts import render, redirect

# Create your views here.

from .forms import Registerform, Loginform, CustomForgotPasswordForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import Multiuser  # your custom user model
from django.contrib.auth.forms import PasswordChangeForm


def home_view(request):
    return render(request, 'homecontent.html')

def login_view(request):
    form = Loginform(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
                # authenticate(username='john') so instead of john we have our variable name, thi function is to check username and password only
            if user is not None:   # checks if authenticate() function has successfully returned user object then user is not none
                login(request, user)   # creates a session for the user so they stay logged in across pages
                return redirect('n_home')
            else:
                msg = 'Invalid Credentials'
        else:
            msg = 'Error validating form'
    return render(request, 'login.html', {'form': form, 'msg': msg})

def register_view(request):
    msg = None
    if request.method == "POST":
        form = Registerform(request.POST)  # when submit form is requested
        if form.is_valid():
            user = form.save(commit=False)
            # optionally lowercase answer
            user.security_answer = form.cleaned_data['security_answer'].lower()
            user.save()
            msg = 'User Created'
            return redirect('n_login')
        else:
            msg = 'Form is not valid'
    else:
        form = Registerform()  # empty form, when no submit 
    return render(request, 'register.html', {'form': form, 'msg': msg})


def logout_view(request):
    logout(request)
    return redirect("n_home")

def changepwd_view(request):
    msg = None
    if request.method == 'POST':
        form = PasswordChangeForm(user= request.user, data= request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            msg = 'Password changed successfully'
            return redirect('n_profile')
    else:
        form = PasswordChangeForm(user= request.user)
    return render(request, 'changepwd.html', {'form': form, 'msg': msg})


def forgotpwd_view(request):
    context = {'form': CustomForgotPasswordForm()}
    
    if request.method == 'POST':
        print("REQUEST POST DATA:", request.POST) 
        form = CustomForgotPasswordForm(request.POST)
        context['form'] = form
        
        # Validate form first to access cleaned data
        if form.is_valid():
            username = form.cleaned_data['username']
            security_answer = form.cleaned_data.get('security_answer')
            new_password = form.cleaned_data.get('new_password')
            confirm_password = form.cleaned_data.get('confirm_password')

            try:
                user = Multiuser.objects.get(username=username)
            except Multiuser.DoesNotExist:
                form.add_error('username', 'User not found')
                return render(request, 'forgotpwd.html', context)

            # First step: Only username provided → show security question
            if username and not security_answer and not new_password:
                context['show_question'] = True
                context['question'] = user.security_question
                context['username'] = username
                return render(request, 'forgotpwd.html', context)

            # Second step: Username + Answer → check answer
            if username and security_answer and not new_password:
                if security_answer.lower() != user.security_answer.lower():
                    form.add_error('security_answer', 'Incorrect answer')
                else:
                    # Correct answer → show password fields 
                    context['show_password_fields'] = True
                    context['question'] = user.security_question
                    context['username'] = username
                return render(request, 'forgotpwd.html', context)

            # Final step: Set new password
            
            if username and security_answer and new_password:
                if security_answer.lower() != user.security_answer.lower():
                    form.add_error('security_answer', 'Incorrect answer')
                    return render(request, 'forgotpwd.html', context)
                
                if new_password != confirm_password:
                    form.add_error('confirm_password', "Passwords do not match.")
                    return render(request, 'forgotpwd.html', context)
                
                # Update the password
                user.set_password(new_password)
                user.save()
                print(f"Password successfully updated for user: {user.username}")
                return redirect('n_login')
            
        else:
            # If form not valid (e.g., missing fields), just return with errors
            return render(request, 'forgotpwd.html', context)
        
    return render(request, 'forgotpwd.html', context)


def profile_view(request):
    return render(request, 'profile.html')

