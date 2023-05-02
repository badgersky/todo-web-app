from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={
            'name': 'username',
            'placeholder': 'username',
        })
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'name': 'password',
            'placeholder': 'password',
        })
    )

    class Meta:
        fields = ('username', 'password')
