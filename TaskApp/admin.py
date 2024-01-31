# task_assignment/admin.py
from django.contrib import admin
from .models import *

admin.site.register(Task)
admin.site.register(Goals)
admin.site.register(ContactMessage)
admin.site.register(Admin)
admin.site.register(Register_table)
admin.site.register(UserTaskImage)
admin.site.register(Blog)

