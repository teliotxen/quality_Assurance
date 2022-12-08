from django import forms
from .models import Questionary


class AnswerForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea, required=False)
    review = forms.BooleanField(required=False)
    TAG_SELECT = (
        ('work', '정상작동'),
        ('error', '오류'),
        ('reported', '보고된 오류'),
    )
    selection = forms.ChoiceField(required=True, choices=TAG_SELECT)

class QuestionaryForm(forms.ModelForm):
    class Meta:
        model = Questionary
        fields = ['title', 'project', 'order', 'main_category', 'sub_category','questionary', 'charge', 'image']


class QuestionaryFormInTask(forms.ModelForm):
    class Meta:
        model = Questionary
        fields = ['title', 'questionary', 'image']