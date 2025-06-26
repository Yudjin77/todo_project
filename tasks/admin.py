from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'publish_status', 'current_status', 'date')

admin.site.register(Task, TaskAdmin)

# Register your models here.
