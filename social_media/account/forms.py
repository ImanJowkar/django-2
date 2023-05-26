from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserRegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="password",widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'your_Password'}))
    password2 = forms.CharField(label="confirmed password",widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'your_Password'}))
    
    
    def clean(self):
        cd = super().clean()
        p1 = cd.get('password1')
        p2 = cd.get('password2')

        if p1 and p2 and p1 != p2:
            raise ValidationError("passwords must match")
            



    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError("This username is already exists.")
        
        return username

    
    
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError("This email address is already exists.")
        
        return email
    

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'your_Password'}))
