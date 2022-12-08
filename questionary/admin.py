from django.contrib import admin
from questionary.models import Questionary, Checker
from sprint.models import TestSet, Scenario, Task


class CheckerAdmin(admin.ModelAdmin):
    list_display = (
        'Question_number', 'user', 'selection', 'description', 'review'
    )
    list_display_links = ('user', 'Question_number')
    list_editable = ['review']
    list_filter = ['category', 'main_category', 'sub_category',  'selection', 'user', 'review']
    # list_per_page = 20


class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'project', 'order', 'questionary',
    )
    # list_display_links = ('project', 'main_category', 'sub_category', 'tag')
    # list_editable = [ 'main_category', 'sub_category', 'questionary', 'tag']
    list_filter = []
    # list_per_page = 10


admin.site.register(Checker, CheckerAdmin)
admin.site.register(Questionary, QuestionAdmin)




