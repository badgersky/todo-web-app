from django.urls import path

from . import views

app_name = 'tasks'

urlpatterns = [
    path('add/', views.AddTask.as_view(), name='add'),
    path('list/', views.DisplayTasks.as_view(), name='list'),
    path('delete/<pk>/', views.DeleteTask.as_view(), name='delete'),
    path('edit/<pk>/', views.EditTask.as_view(), name='edit'),
    path('delete/', views.DeletePastTasks.as_view(), name='delete-many'),
]
