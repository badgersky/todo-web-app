from django.urls import path

from . import views

app_name = 'tasks'

urlpatterns = [
    path('add/', views.AddTask.as_view(), name='add'),
]
