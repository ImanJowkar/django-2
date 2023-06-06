from django import http
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from home.models import Post
from django.contrib.auth import views as auth_views
from . import forms
from .models import Relation


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
    
    
    
    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)
    
    
    
    
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
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            messages.error(request, "username or password is incorrect")
        return render(request, self.template_name, {'form': form})
    
    

class UserLogoutView(LoginRequiredMixin, View):
    
    # login_url = '/account/login'
    def get(self, request):
        logout(request)
        messages.success(request, f"you logged out successfully.", extra_tags='success')
        return redirect('home:home')
    
    
class UserProfileView(LoginRequiredMixin, View):
    
    def get(self, request, user_id):
        is_following = False
        user = get_object_or_404(User,id=user_id)
        posts = user.posts.all()
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            is_following = True
        return render(request, 'account/profile.html', {'user': user, 'posts': posts, 'is_following': is_following})



class UserPasswordRestView(auth_views.PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password-reset-done')
    email_template_name = 'account/password_reset_email.html'
    

class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'
    
class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password-reset-complete')
    

class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'
    
    
    
    
class UserFollowView(LoginRequiredMixin,View):
    
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user = request.user, to_user = user)
        if relation.exists():
            messages.error(request, "you are already following this user", extra_tags='error')
        else:
            Relation.objects.create(from_user=request.user, to_user=user)
            messages.success(request, "you followed this user", extra_tags='success')
        return redirect('account:user-profile', user.id)
    
    
    
    
class UserUnFollowView(LoginRequiredMixin,View):
    
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user = request.user, to_user = user)
        if relation.exists():
            relation.delete()
            messages.success(request,"you unfollowed this user", extra_tags='success')
        else:
            messages.error('you are not following this user', extra_tags='error')
        return redirect('account:user-profile', user.id)    
    