from django.contrib import admin
from .models import TestSet, Scenario, Task
# Register your models here.
admin.site.register(TestSet)
admin.site.register(Scenario)
admin.site.register(Task)
