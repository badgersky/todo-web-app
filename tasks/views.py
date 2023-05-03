import datetime

from django.http import HttpResponse
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


class DisplayTasks(View):

    def get(self, request):
        if request.user.is_authenticated:
            today = datetime.date.today()

            tasks = models.Task.objects.filter(user_id=request.user.id).order_by('date')
            return render(request, 'tasks/list-tasks.html', {'tasks': tasks, 'today': today})


class DeleteTask(View):

    def get(self, request, task_id):
        try:
            task = models.Task.objects.get(pk=int(task_id))
        except models.Task.DoesNotExist:
            return redirect(reverse('tasks:list'))
        else:
            task.delete()
            return redirect(reverse('tasks:list'))


class EditTask(View):

    def get(self, request, task_id):
        try:
            task = models.Task.objects.get(pk=task_id)
        except models.Task.DoesNotExist:
            return redirect(reverse('tasks:list'))

        form = forms.EditTaskForm(data={'title': task.title, 'description': task.description, 'date': task.date})
        return render(request, 'tasks/edit-task.html', {'form': form})

    def post(self, request, task_id):
        form = forms.EditTaskForm(request.POST)

        if form.is_valid():
            try:
                task = models.Task.objects.get(pk=task_id)
            except models.Task.DoesNotExist:
                return redirect(reverse('tasks:list'))
            else:
                task.date = form.cleaned_data.get('date')
                task.title = form.cleaned_data.get('title')
                task.description = form.cleaned_data.get('description')

                task.save()
                return redirect(reverse('tasks:list'))

        return render(request, 'tasks/edit-task.html', {'form': form})
