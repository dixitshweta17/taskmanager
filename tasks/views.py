from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth import get_user_model, authenticate
from tasks.models import Task
from .serializers import TaskSerializer
from django.shortcuts import render, redirect


class TaskCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(f"Current user: {request.user}")
        tasks = Task.objects.filter(user=request.user)
        print(f"Tasks for user: {tasks}")
        return render(request, 'task_create.html', {'tasks': tasks})

    def post(self, request):
        serializer = TaskSerializer(data=request.data, context={'request': request})
        print("serializer", serializer)
        if serializer.is_valid():
            print("Validated data:", serializer.validated_data)
            serializer.save()
            return redirect('task-list-create')
        else:
            print("Serializer errors:", serializer.errors)
        tasks = Task.objects.filter(user=request.user)
        return render(request, 'task_create.html', {'tasks': tasks, 'errors': serializer.errors})
    
   
class TaskListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(f"Current user: {request.user}")
        tasks = Task.objects.filter(user=request.user)
        print(f"Tasks for user: {tasks}")
        return render(request, 'task_list.html', {'tasks': tasks})
    

    def post(self, request):
        serializer = TaskSerializer(data=request.data, context={'request': request})
        print("serializer", serializer)
        if serializer.is_valid():
            print("Validated data:", serializer.validated_data)
            serializer.save()
            return redirect('task-list-create')
        else:
            print("Serializer errors:", serializer.errors)
        tasks = Task.objects.filter(user=request.user)
        return render(request, 'task_list.html', {'tasks': tasks, 'errors': serializer.errors})
    

class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Task.objects.get(pk=pk, user=user)
        except Task.DoesNotExist:
            return None

    def get(self, request, pk):
        task = self.get_object(pk, request.user)
        if task:
            return render(request, 'task_detail.html', {'task': task})
        return redirect('task-list-create')

    def put(self, request, pk, format=None):
        task = self.get_object(pk, request.user)
        if task:
            serializer = TaskSerializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_200_OK)
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, pk):
        task = self.get_object(pk, request.user)
        if task:
            if request.POST.get('_method') == 'DELETE':
                task.delete()
                return redirect('task-list-create')
            serializer = TaskSerializer(task, data=request.POST)
            if serializer.is_valid():
                serializer.save()
                return redirect('task-detail', pk=task.pk)
            return render(request, 'task_detail.html', {'task': task, 'errors': serializer.errors})
        return redirect('task-list-create')

   