from django.contrib import admin
from .models import Task

# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'priority', 'completed', 'created_at']
    list_filter = ['priority', 'completed', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['completed', 'priority']
