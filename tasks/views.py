from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from . import forms
import datetime
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
            today = datetime.date.today()

            date = form.cleaned_data.get('date')
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')

            if date <= today:
                return redirect(reverse('tasks:add'))

            new_task = models.Task.objects.create()
            new_task.user = request.user
            new_task.title = title
            new_task.description = description
            new_task.save()
            return redirect(reverse('home:home'))

        return redirect(reverse('tasks:add'))
