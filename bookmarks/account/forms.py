from django import forms
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)# PasswordInput widget to render the password HTML element. This will include type="password" in the HTML so that the browser treats it as a password input.


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User # use User model for this form
        fields = ('username', 'first_name', 'email') # Include model fields

    def clean_password2(self): # This check is done when you validate the form by calling its is_valid() You can provide a clean_<fieldname>() method to any of your form fields in order to clean the value or raise form validation errors for a specific field
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')

