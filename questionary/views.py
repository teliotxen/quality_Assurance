import csv

from django.http import HttpResponse
from django.shortcuts import get_object_or_404,render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from sprint.models import TestSet, Scenario, Task
from questionary.models import Questionary, Checker
from django.views.generic import ListView
from questionary.forms import AnswerForm, QuestionaryForm, QuestionaryFormInTask


@login_required
def main_category(request):
    data = TestSet.objects.all()
    return render(request, 'questionary/category.html', context={'data': data})


@method_decorator(login_required, name="dispatch")
class QuestionaryView(ListView):
    template_name = 'questionary/questionary.html'
    context_object_name = 'question_list'

    def get_context_data(self, **kwargs):
        # 생성된 context는 Template으로 전달됨.
        context = super().get_context_data(**kwargs)
        obj = TestSet.objects.get(pk=self.kwargs['pk'])
        context['pid'] = self.kwargs['pk']
        context['theid'] = obj.title

        questions = Questionary.objects.filter(project=obj)
        review = Checker.objects.filter(user=self.request.user, category=obj)
        checker_list = review.values()

        error_list = []
        complete_list = []
        for item in review:
            if not item.questions in error_list:
                if item.selection == 'error':
                    error_list.append(int(item.Question_number.pk))
                elif item.selection == 'work':
                    complete_list.append(int(item.Question_number.pk))

        review_list = []
        if len(checker_list) != 0:
            for item in checker_list:
                if item['Question_number_id'] in review_list:
                    pass
                else:
                    review_list.append(item['Question_number_id'])
        #중복제거작업
        context['total_numb'] = questions
        context['complete_list'] = complete_list
        context['complete_numb'] = len(set(complete_list + error_list))
        context['error_list'] = error_list
        context['answered'] = review_list
        self.request.session['answered'] = review_list

        return context

    def get_queryset(self):

        pk_id = self.kwargs['pk']
        data = Questionary.objects.filter(project=pk_id)

        try:
            if self.request.session['questionary_list']:
                pass
            else:
                dict_data = Questionary.objects.filter(project=pk_id).values()
                data_list = []
                for item in dict_data:
                    data_list.append(item['id'])
                self.request.session['questionary_list'] = data_list
        except:
            dict_data = Questionary.objects.filter(project=pk_id).values()
            data_list = []
            for item in dict_data:
                data_list.append(item['id'])
            self.request.session['questionary_list'] = data_list
        return data


@login_required
def detail(request, pk):
    question = get_object_or_404(Questionary, pk=pk)
    task = Task.objects.get(pk=question.sub_category_id)
    result = Checker.objects.filter(Question_number=pk)
    form = AnswerForm()
    preOverAll = Questionary.objects.filter(project=question.project)
    overall = []
    for item in preOverAll:
        overall.append(item.pk)

    userinfo = request.user

    if request.method == 'POST':
        '''form 변수 지장'''
        form = AnswerForm(request.POST, request.FILES)
        search_keys = form.data.dict().keys()
        userinfo = request.user
        if len(search_keys) == 1:
            pass
        else:
            '''post에서 가져온 form 값 변수 저장'''
            user = request.user
            if 'workable' in search_keys:
                workable = True
            else:
                workable = False
            description = form.data['description']

            '''checker 저장'''
            checker = Checker()
            checker.Question_number = question
            checker.questions = question.questionary
            checker.category = task.set.set
            checker.main_category = task.set
            checker.sub_category = task
            checker.charge = task.charge
            checker.user = user
            checker.selection = form.data['selection']
            checker.description = description
            checker.save()
            url_pk = question.pk
        # return redirect(f'questions/{url_pk}')
        return redirect('detail', url_pk)
    else:
        return render(request, 'questionary/detail.html', context={'questionary':question, 'form':form, 'result': result, 'overall':overall,'userinfo':userinfo, 'task':task })


@login_required
def comment_delete(request, **kwargs):
    pk_id = kwargs['pk']
    checker_object = Checker.objects.get(pk=pk_id)
    parent_pk = checker_object.Question_number.pk

    if request.method == 'POST':
        checker_object.delete()
        return redirect('detail', parent_pk)
    return render(request, 'questionary/deletion.html', context={'pk_id':parent_pk})


@method_decorator(login_required, name="dispatch")
class IssueTracker(ListView):
    template_name = 'questionary/issue.html'
    context_object_name = 'issue_list'

    def get_context_data(self, **kwargs):
        # 생성된 context는 Template으로 전달됨.
        pk_id = self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        data = Checker.objects.filter(selection='error',category_id=pk_id).order_by('review', '-updated_at')
        context['issues'] = data

        return context

    def get_queryset(self):
        # pk_id = self.kwargs['pk']
        data = Checker.objects.filter(selection='error')
        return data


@login_required
def comment_confirm(request, **kwargs):
    pk_id = kwargs['pk']
    checker_object = Checker.objects.get(pk=pk_id)
    parent_pk = checker_object.category_id

    if request.method == 'POST':
        if checker_object.review == True:
            checker_object.review = False
            checker_object.save()
        else:
            checker_object.review = True
            checker_object.save()
        return redirect('issue', parent_pk)
    return render(request, 'questionary/confirm.html', context={'pk_id': parent_pk})


@login_required
def questionary_input(request, pk):
    form = QuestionaryFormInTask()
    task = Task.objects.get(pk=pk)
    context = {'form':form, 'task':task}
    if request.method == 'POST':

        upload = QuestionaryFormInTask(request.POST, request.FILES)
        if upload.is_valid():
            count = Questionary.objects.filter(sub_category=task)
            if len(count) == 0:
                cntnumb = 1
            else:
                count_list =[]
                for item in count.values_list('order'):
                    count_list.append(int(item[0]))
                cntnumb = max(count_list)+1

            data = Questionary()

            data.index = cntnumb
            data.order = cntnumb
            data.project = task.set.set
            data.main_category = task.set
            data.sub_category = task
            data.charge = task.charge
            data.title = upload.cleaned_data['title']
            data.questionary = upload.cleaned_data['questionary']

            try:
                data.image = request.FILES['image']
            except:
                pass

            data.save()
            return redirect('task_detail', task.pk)

    return render(request, 'questionary/form.html', context)



@login_required
def questionary_update(request, pk):
    qa = Questionary.objects.get(pk=pk)
    form = QuestionaryForm(instance=qa)
    task = Task.objects.get(pk=qa.sub_category.pk)
    context = {'form':form, 'task':task}
    if request.method == 'POST':

        upload = QuestionaryFormInTask(request.POST, request.FILES)
        if upload.is_valid():
            qa.title = upload.cleaned_data['title']
            qa.questionary = upload.cleaned_data['questionary']

            try:
                qa.image = request.FILES['image']
            except:
                pass

            qa.save()
            return redirect('detail', qa.pk)

    return render(request, 'questionary/form.html', context)

