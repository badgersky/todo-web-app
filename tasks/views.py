import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView

from tasks.forms import AddTaskForm


class AddTask(LoginRequiredMixin, CreateView):

    login_url = reverse_lazy('users:login')
    form_class = AddTaskForm
    template_name = 'tasks/add-task.html'
    success_url = reverse_lazy('tasks:list')


class DisplayTasks(View):

    def get(self, request):
        if request.user.is_authenticated:
            today = datetime.date.today()

            tasks = models.Task.objects.filter(user_id=request.user.id).order_by('date')
            paginator = Paginator(tasks, 25)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            return render(request, 'tasks/list-tasks.html', {'page_obj': page_obj, 'today': today})

        return redirect(reverse('users:login'))


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


class DeletePastTasks(View):

    def get(self, request):
        if request.user.is_authenticated:
            tasks = models.Task.objects.filter(date__lt=datetime.date.today(), user=request.user)

            tasks.delete()
            return redirect(reverse('tasks:list'))

        return redirect(reverse('users:login'))
