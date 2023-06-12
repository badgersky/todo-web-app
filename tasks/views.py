import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView

from tasks.forms import AddTaskForm
from tasks.models import Task


class AddTask(LoginRequiredMixin, CreateView):

    login_url = reverse_lazy('users:login')
    form_class = AddTaskForm
    template_name = 'tasks/add-task.html'
    success_url = reverse_lazy('tasks:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DisplayTasks(LoginRequiredMixin, ListView):

    login_url = reverse_lazy('users:login')
    model = Task
    template_name = 'tasks/list-tasks.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        today = datetime.date.today()

        tasks = Task.objects.filter(user=self.request.user)
        paginator = Paginator(tasks, 20)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context['today'] = today
        context['page_obj'] = page_obj
        return context


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
