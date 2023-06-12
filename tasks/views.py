import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView

from tasks.forms import AddTaskForm, EditTaskForm
from tasks.models import Task
from tasks.permissions import TaskCreatorRequiredMixin


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


class DeleteTask(LoginRequiredMixin, TaskCreatorRequiredMixin, View):

    def get(self, request, pk):
        try:
            task = Task.objects.get(pk=int(pk))
        except Task.DoesNotExist:
            return redirect(reverse('tasks:list'))
        else:
            task.delete()
            return redirect(reverse('tasks:list'))


class EditTask(LoginRequiredMixin, TaskCreatorRequiredMixin, UpdateView):
    template_name = 'tasks/edit-task.html'
    model = Task
    form_class = EditTaskForm
    success_url = reverse_lazy('tasks:list')
    login_url = reverse_lazy('users:login')


class DeletePastTasks(LoginRequiredMixin, View):
    login_url = reverse_lazy('users:login')

    def get(self, request):
        tasks = Task.objects.filter(date__lte=datetime.date.today(), user=request.user)

        tasks.delete()
        return redirect(reverse('tasks:list'))


class MarkAsDone(LoginRequiredMixin, TaskCreatorRequiredMixin, View):
    login_url = reverse_lazy('users:login')

    def get(self, request, pk):
        task = Task.objects.get(user=request.user, pk=pk)
        task.is_done = True
        task.save()
        return redirect(reverse('tasks:list'))


class DeleteDoneTasks(LoginRequiredMixin, View):
    login_url = reverse_lazy('users:login')

    def get(self, request):
        tasks = Task.objects.filter(is_done=True, user=request.user)

        tasks.delete()
        return redirect(reverse('tasks:list'))
