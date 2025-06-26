from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, ListView, DetailView

from tasks.forms import TaskForm
from tasks.models import Task, TaskVote
from rest_framework import generics, permissions

from tasks.permissions import IsOwnerOrReadOnly
from tasks.serializer import TaskSerializer


class TaskListView(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tasks/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sort = self.request.GET.get('sort', 'new')
        query = self.request.GET.get('q')
        popular_list = Task.objects.annotate(
                total_likes=Sum('votes__vote')
            ).filter(publish_status=True).order_by('-total_likes').select_related('category')

        if query: #Поисковик
            context['tasks'] = popular_list.filter(title__icontains=query)
        elif sort == 'popular': #Популярные
            context['tasks'] = popular_list
        else: #По дате добавления(Новые)
            context['tasks'] = Task.objects.filter(publish_status=True).order_by('-date').select_related('category')

        context['sort'] = sort
        return context

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/add_task.html'
    success_url = reverse_lazy('tasks:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaskDetailView(DetailView, LoginRequiredMixin):
    model = Task
    context_object_name = 'task'
    template_name = 'tasks/task_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        context['likes'] = task.votes.filter(vote=TaskVote.LIKES).count()
        context['dislikes'] = task.votes.filter(vote=TaskVote.DISLIKES).count()
        return context

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        vote_value = request.POST.get('vote')
        if vote_value in ['like', 'dislike']:
            vote_int = TaskVote.LIKES if vote_value == 'like' else TaskVote.DISLIKES
            TaskVote.objects.update_or_create(
                task=task,
                user=request.user,
                defaults={'vote': vote_int}
            )
        return redirect('tasks:task_detail', slug=task.slug)

class MyTaskListView(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tasks/my_tasks.html'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class TaskEditAPIView(generics.UpdateAPIView): #TaskDetailView
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'slug'
    permission_classes = (IsOwnerOrReadOnly, )

























