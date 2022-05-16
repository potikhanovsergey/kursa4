from django.contrib import admin
from import_export.admin import ExportActionMixin

# Register your models here.

from .models import (Post, Comment, Service, Employee, ClientService,
Client)

class PostsExcel(ExportActionMixin, admin.ModelAdmin):
    list_display = ('author', 'title', 'description', 'date')

admin.site.register(Post, PostsExcel)
admin.site.register(Comment)
admin.site.register(Service)
admin.site.register(Employee)
admin.site.register(ClientService)
admin.site.register(Client)