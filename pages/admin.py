from django.contrib import admin

# Register your models here.

from .models import (Post, Comment, Service, Employee, ClientService,
Client)

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Service)
admin.site.register(Employee)
admin.site.register(ClientService)
admin.site.register(Client)