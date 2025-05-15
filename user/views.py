from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from user.forms import CustomUserCreationForm,CustomAuthenticationForm
from django.contrib.auth import login,logout
from userprofile.models import UserProfile

def registration_view(request):
    print(request.method)
    if request.method == "POST":
        print(request.POST)
        fm = CustomUserCreationForm(request.POST)
        print(fm.is_valid())
        if fm.is_valid():
            user = fm.save()
            created_profile = UserProfile.objects.create(user=user)
            return redirect('/login')
        else:
            # print(fm.errors)
            context = {"form": fm}
            return render(request, 'user/signup.html', context=context)
    else:
        fm = CustomUserCreationForm()
        context = {"form": fm}
        return render(request, 'user/signup.html', context=context)


def login_view(request):
    # print(request.method)
    if request.method == "POST":
        print(request.POST)
        fm = CustomAuthenticationForm(data=request.POST)
        print(fm.is_valid())
        if fm.is_valid():
            user = fm.get_user()
            login(request,user)
            return redirect('/')
        else:
            context = {"form": fm}
            print(fm.errors)
            return render(request, 'user/login.html', context=context)
    else:
        fm = CustomAuthenticationForm()
        context = {"form": fm}
        return render(request, 'user/login.html', context=context)
    
def logout_view(request):
    logout(request)
    return redirect('/')


def check_login_view(request):
    if request.user.is_authenticated:
        return True
    else:
        return False
