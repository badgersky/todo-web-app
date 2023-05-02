from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from . import forms
from . import models


class AddTask(View):

    def get(self, request):
        if request.user.is_authenticated:
            form = forms.AddTaskForm
            return render(request, 'tasks/add-task.html', {'form': form})

        return redirect(reverse('users:login'))

    def post(self, request):
        form = forms.AddTaskForm(request.POST)

        if form.is_valid():
            user = request.user
            date = form.cleaned_data.get('date')
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')

            new_task = models.Task()
            new_task.date = date
            new_task.user = user
            new_task.title = title
            new_task.description = description
            new_task.save()
            return redirect(reverse('home:home'))

        return render(request, 'tasks/add-task.html', {'form': form})
