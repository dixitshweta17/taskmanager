from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status_choice', 'due_date']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        else:
            raise serializers.ValidationError("User context is required for task creation.")
        return Task.objects.create(user=user, **validated_data)

    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.status_choice = validated_data.get('status_choice', instance.status_choice)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.save()
        # print(instance)
        return instance   