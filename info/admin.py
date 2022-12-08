from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, DevTeam

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(DevTeam)
# UserAdmin.fieldsets += (("Custom fields", {"fields": ("parent","phone","name","birthday","school","gender","identification","get_time", 'router')}),)