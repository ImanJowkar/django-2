from typing import Any
from django import http
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from . import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

# Create your views here.



class UserRegisterView(View):
    
    form_class = forms.UserRegistrationForm
    template_name = 'account/register.html'
    
    
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        else:
            return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})
    
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(username=cd['username'],password=cd['password1'], email=cd['email'])
            messages.success(request, f'Account created for {cd["username"]} successfully',extra_tags='success')
            return redirect('home:home')
        return render(request, self.template_name, context={'form': form})



class UserLoginView(View):

    form_class = forms.UserLoginForm
    template_name = 'account/login.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, 'You are already logged in', extra_tags='warning')
            return redirect('home:home')
        else:
            return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, context={'form': form})
    
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, f"{cd['username']} logged in successfully", extra_tags='success')
                return redirect('home:home')
            messages.error(request, "username or password is incorrect")
        return render(request, self.template_name, {'form': form})
    
    

class UserLogoutView(LoginRequiredMixin, View):
    # login_url = '/account/login'
    def get(self, request):
        logout(request)
        messages.success(request, f"you logged out successfully.", extra_tags='success')
        return redirect('home:home')