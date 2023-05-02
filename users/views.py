from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from . import forms


class LoginView(View):

    def get(self, request):
        form = forms.LoginForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = forms.LoginForm(request.POST)

        if form.is_valid():
            login(request, request.user)
            return redirect(reverse('users:login', kwargs={'form': form}))

        return redirect(reverse('home:home'))
