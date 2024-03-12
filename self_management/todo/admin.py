from django.contrib import admin
from .models import Todo, Category

# Register your models here.

class TodoAdmin(admin.ModelAdmin):
  list_filter = ["due", "start"]
admin.site.register(Todo, TodoAdmin)
admin.site.register(Category)
