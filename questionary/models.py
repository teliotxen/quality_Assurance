from django.db import models
from django import forms

# Create your models here.


class Questionary(models.Model):
    title = models.CharField(max_length=40, null=True)
    project = models.ForeignKey('sprint.TestSet', on_delete=models.CASCADE, null=True)
    index = models.CharField(max_length=100)
    order = models.CharField(max_length=10)
    main_category = models.ForeignKey('sprint.Scenario', on_delete=models.CASCADE)
    sub_category = models.ForeignKey('sprint.Task', on_delete=models.CASCADE)
    questionary = models.TextField(blank=True)
    charge = models.ForeignKey('info.DevTeam', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.order


def default_selection(value):
    if value == 'default':
        raise forms.ValidationError('항목을 선택하세요!')


class Checker(models.Model):
    Question_number = models.ForeignKey("Questionary", on_delete=models.CASCADE)
    questions = models.TextField(blank=True)
    category = models.ForeignKey('sprint.TestSet', on_delete=models.CASCADE, null=True)
    main_category = models.CharField(max_length=20, null=True)
    sub_category = models.CharField(max_length=20, null=True)
    charge = models.ForeignKey('info.DevTeam',on_delete=models.CASCADE, null=True)
    user = models.CharField(max_length=20, null=True)
    TAG_SELECT = (
        ('reported', 'reported'),
        ('error', 'error'),
        ('work', 'work'),
    )
    selection = models.CharField(max_length=10, choices=TAG_SELECT, null=True, validators=[default_selection])
    description = models.TextField(blank=True)
    review = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


    def __str__(self):
        return self.Question_number.order


