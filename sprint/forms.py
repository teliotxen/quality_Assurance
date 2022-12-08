from django import forms
from info.models import DevTeam
from .models import TestSet, Scenario, Task


class TestSetForm(forms.ModelForm):

    class Meta:
        model = TestSet
        fields =['title', 'contents']


class ScenarioForm(forms.ModelForm):

    class Meta:
        model = Scenario
        fields = ['title', 'contents','image']


class DateInput(forms.DateInput):
    input_type = 'date'


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'contents', 'start_date', 'due_date', 'charge', 'image']

