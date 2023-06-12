from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from . import forms


class LoginView(View):

    def get(self, request):
        form = forms.LoginForm(request)
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = forms.LoginForm(request, request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('home:home'))

        return render(request, 'users/login.html', {'form': form})


class RegistrationView(View):

    def get(self, request):
        form = forms.RegistrationForm()
        return render(request, 'users/registration.html', {'form': form})

    def post(self, request):
        form = forms.RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse('users:login'))

        return render(request, 'users/registration.html', {'form': form})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect(reverse('home:home'))
