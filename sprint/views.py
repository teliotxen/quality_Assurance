import csv

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.generic import ListView
from .models import TestSet, Task, Scenario
from info.models import DevTeam
from sprint.forms import TestSetForm, TaskForm, ScenarioForm
from questionary.forms import QuestionaryFormInTask
from questionary.models import Questionary, Checker

"""form view"""
@login_required
def task_input_form(request, pk):
    form = TaskForm()
    data = Scenario.objects.get(pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        task = Task()
        task.test_set = data.set
        task.set = data
        task.title = form['title'].data
        task.contents = form['contents'].data
        task.start_date = form['start_date'].data
        task.due_date = form['due_date'].data
        int_pk = form['charge'].data
        task.charge = DevTeam.objects.get(pk=int_pk)

        try:
            task.image = request.FILES['image']

        except:
            pass
        task.save()
        if not data.tasks.contains(task):
            data.tasks.add(task)

        url = '/sprint/tasks/'+str(pk)+'/'
        return redirect(url)

    return render(request, 'sprint/form.html', context={'form': form, 'data': data})

@login_required
def scenario_input_form(request, pk):
    form = ScenarioForm()
    data = TestSet.objects.get(pk=pk)
    if request.method == 'POST':
        form = ScenarioForm(request.POST, request.FILES)
        scenario = Scenario()
        scenario.set = TestSet.objects.get(pk=pk)
        scenario.title = form['title'].data
        scenario.contents = form['contents'].data
        try:
            scenario.image = request.FILES['image']
        except:
            pass
        scenario.save()

        url = '/sprint/'+str(pk)+'/'
        return redirect(url)
    return render(request, 'sprint/form.html', context={'form': form, 'data':data})

@login_required
def test_set_input_form(request):
    form = TestSetForm()
    if request.method == 'POST':
        form = TestSetForm(request.POST)
        test_set = TestSet()
        test_set.title = form['title'].data
        test_set.contents = form['contents'].data
        test_set.save()
        return redirect('sprint')

    return render(request, 'sprint/form.html', context={'form': form})

@login_required
def scenario_view(request, pk):
    data = TestSet.objects.get(pk=pk)
    data_list = Scenario.objects.filter(set=data)
    return render(request, 'sprint/scenario.html', context={'test_set': data, 'data_list': data_list})


"""general view"""


@login_required
def task_detail_view(request, pk):
    data = Task.objects.get(pk=pk)
    load_questions = Questionary.objects.filter(sub_category=data)

    return render(request, 'sprint/task_detail.html', context={'data': data, 'questions':load_questions})


@login_required
def task_view(request, pk):
    data = Scenario.objects.get(pk=pk)
    request.session['selected'] = pk

    load_task = data.tasks.all()
    # load_task = Task.objects.filter(set=data)
    return render(request, 'sprint/tasks.html', context={'test_set': data, 'data_list': load_task})


@method_decorator(login_required, name="dispatch")
class TestSetView(ListView):
    template_name = 'sprint/sprint.html'
    context_object_name = 'sprint_list'
    model = TestSet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.request.session['pageInfo'] = []
        return context


"""update view"""
@login_required
def scenario_update_view(request, pk):
    data = Scenario.objects.get(pk = pk)
    form = ScenarioForm(instance=data)
    if request.method == "POST":
        form = ScenarioForm(request.POST, request.FILES)
        if form.is_valid():
            data.title = form.cleaned_data['title']
            data.contents = form.cleaned_data['contents']
            try:
                data.image = request.FILES['image']
            except:
                pass
            data.save()

            # url = '/sprint/' + str(pk) + '/'
            url = '/sprint/tasks/' + str(pk) + '/'
            return redirect(url)

    return render(request, 'sprint/form.html', context={'form':form, 'data':data})

@login_required
def task_update_view(request, pk):
    data = Task.objects.get(pk=pk)
    input_url_data = data.set.pk
    form = TaskForm(instance=data)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            data.title = form.cleaned_data['title']
            data.contents = form.cleaned_data['contents']
            data.start_date = form.cleaned_data['start_date']
            data.due_date = form.cleaned_data['due_date']
            int_pk = form.cleaned_data['charge']
            data.charge = DevTeam.objects.get(username=int_pk)

            try:
                data.image = request.FILES['image']

            except:
                pass
            data.save()
            url = '/sprint/tasks/' + str(input_url_data) + '/'
            return redirect(url)

    return render(request, 'sprint/form.html', context={'form': form, 'data':data})


@login_required
def test_set_update_view(request, pk):
    data = TestSet.objects.get(pk=pk)
    form = TestSetForm(instance=data)
    if request.method == "POST":
        form = TestSetForm(request.POST, request.FILES)
        if form.is_valid():
            data.title = form.cleaned_data['title']
            data.contents = form.cleaned_data['contents']
            data.save()

            url = '/sprint/'
            return redirect(url)

    return render(request, 'sprint/form.html', context={'form':form, 'data':data})

"""
delete view
"""
@login_required
def task_delete_view(request, pk):
    data = Task.objects.get(pk=pk)
    if request.method == "POST":
        set_id = data.set.pk
        data.delete()
        return redirect('tasks', set_id)
    return render(request, 'sprint/delete.html',context={'data':data})

@login_required
def scenario_delete_view(request, pk):
    data = Scenario.objects.get(pk=pk)
    if request.method == "POST":
        set_id = data.set.pk
        data.delete()
        return redirect('scenario', set_id)
    return render(request, 'sprint/delete.html',context={'data':data})

@login_required
def test_set_delete_view(request, pk):
    data = TestSet.objects.get(pk=pk)
    if request.method == "POST":
        # set_id = data.pk
        data.delete()
        return redirect('sprint')
    return render(request, 'sprint/delete.html',context={'data':data})


'''download csv view'''


def scenario_csv(request, pk):
    sprint = TestSet.objects.get(pk=pk)
    data = Scenario.objects.filter(set = sprint)

    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="scenario.csv"'},
    )
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    for item in data:
        output = []
        output.append(item.id)
        output.append(item.title)
        output.append(item.contents)
        created_time = item.created_at
        output.append(str(created_time).split(' ')[0])
        writer.writerow(output)

    return response


def tasks_csv(request, pk):
    sprint = TestSet.objects.get(pk=pk)
    data = Task.objects.filter(set__set=sprint)


    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="tasks.csv"'},
    )
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    for item in data:
        output = []
        output.append(item.id)
        output.append(item.set_id)
        output.append(item.title)
        output.append(item.contents)
        output.append(item.charge.username)
        start_date = item.start_date
        output.append(str(start_date).split(' ')[0])
        due_date = item.due_date
        output.append(str(due_date).split(' ')[0])

        writer.writerow(output)

    return response


def qa_csv(request, pk):
    sprint = TestSet.objects.get(pk=pk)
    data = Questionary.objects.filter(project=sprint)
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="qa_items.csv"'},
    )

    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    for item in data:
        output = []
        output.append(str(item.order))
        output.append(str(item.title))
        output.append(str(item.main_category.title))
        output.append(str(item.sub_category.title))
        output.append(str(item.questionary))
        output.append(str(item.charge.username))
        writer.writerow(output)

    return response


def duplicated_task(request,pk):
    scenario = Scenario.objects.get(pk=pk)
    data = Task.objects.filter(test_set = scenario.set)
    if request.method == 'POST':
        result = request.POST.getlist('answer[]')
        for item in result:
            value = Task.objects.get(pk=item)
            scenario.tasks.add(value)

        scenario.save()
        return redirect('tasks', pk)

    return render(request, 'sprint/duplicate.html', context={'data':data, 'pk_num':pk})


def remove_duplicated_task(request,pk):
    scenario_pk = request.session['selected']
    scenario = Scenario.objects.get(pk=scenario_pk)
    if request.method == 'POST':
        task_set = Task.objects.get(pk=pk)
        scenario.tasks.remove(task_set)
        scenario.save()
        return redirect('tasks', scenario_pk)

    return render(request, 'sprint/remove.html',context={'data':scenario })
