from django.contrib import admin
from .models import Contact, Task, Subtask

class SubtaskInline(admin.TabularInline):
    model = Subtask
    extra = 1

class TaskAdmin(admin.ModelAdmin):
    inlines = [SubtaskInline]

admin.site.register(Contact)
admin.site.register(Task, TaskAdmin)
admin.site.register(Subtask)
