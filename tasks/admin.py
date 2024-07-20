from django.contrib import admin
from tasks.models import Task

# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ["user", "title", "description", "status_choice", "due_date"]
admin.site.register(Task, TaskAdmin)