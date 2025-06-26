from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.TaskListView.as_view(), name='home'),
    path('add_task', views.TaskCreateView.as_view(), name='add_task'),
    path('my_tasks/', views.MyTaskListView.as_view(), name='my_tasks'),
    path('<slug:slug>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('api/v1/<slug:slug>/edit', views.TaskEditAPIView.as_view(), name='task_edit')
]