from datetime import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login or Email', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model() #подлючаем стандартную модель(User) Джанго
        fields = ('username', 'password')


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name')
        labels = {
            'email': 'Email',
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }
        widgets = {                           #задаем стили для полей с помощью widgets
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered")
        return email


class ProfileUserForm(forms.ModelForm):

    username = forms.CharField(disabled=True, label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(disabled=True, label='E-mail', widget=forms.TextInput(attrs={'class': 'form-input'}))
    this_year = datetime.today().year
    date_birth = forms.DateField(widget=forms.SelectDateWidget(years=tuple(range(this_year-100, this_year-5))))


    class Meta:
        model = get_user_model()
        fields = ('photo','username', 'email', 'date_birth', 'first_name', 'last_name')
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }



class UserChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))










