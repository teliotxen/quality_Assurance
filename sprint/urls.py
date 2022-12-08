"""qaService URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from sprint import views

urlpatterns = [
    path('', views.TestSetView.as_view(), name='sprint'),
    path('<int:pk>/', views.scenario_view, name='scenario'),
    path('tasks/<int:pk>/', views.task_view, name='tasks'),
    path('task_detail/<int:pk>/', views.task_detail_view, name='task_detail'),
    path('form/test_set/', views.test_set_input_form, name='test_set_input_form'),
    path('form/<int:pk>/scenario/', views.scenario_input_form, name='scenario_input_form'),
    path('form/<int:pk>/task/', views.task_input_form, name='task_input_form'),
    path('detail/<int:pk>', views.task_detail_view, name='sprint_detail'),


    path('form/<int:pk>/testset/update/', views.test_set_update_view, name='test_set_update_form'),
    path('form/<int:pk>/scenario/update/', views.scenario_update_view, name='scenario_update_form'),
    path('form/<int:pk>/task/update/', views.task_update_view, name='task_update_form'),


    path('delete/task/<int:pk>', views.task_delete_view, name='task_delete'),
    path('delete/scenairo/<int:pk>', views.scenario_delete_view, name='scenario_delete'),
    path('delete/testset/<int:pk>', views.test_set_delete_view, name='test_set_delete'),

    path('scenario_csv/<int:pk>/', views.scenario_csv, name='scenario_csv'),
    path('tasks_csv/<int:pk>/', views.tasks_csv, name='tasks_csv'),
    path('qa_csv/<int:pk>/', views.qa_csv, name='qa_csv'),

    path('duplicate/<int:pk>/', views.duplicated_task, name='duplicated_task'),
    path('duplicate/<int:pk>/remove', views.remove_duplicated_task, name='remove_duplicated_task'),
]
