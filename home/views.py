import datetime
from django.shortcuts import render
from django.views import View
from tasks.models import Task


class HomeView(View):

    def get(self, request):
        tasks = Task.objects.filter(user_id=request.user.id, date=datetime.date.today())
        return render(request, 'home/home.html', {'tasks': tasks})
