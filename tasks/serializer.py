from rest_framework import serializers

from tasks.models import Task

class TaskSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255, required=False)
    description = serializers.CharField(required=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault( ))

    class Meta:
        model = Task
        fields = ['title', 'category', 'description', 'publish_status', 'user']