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
from django.contrib import admin
from django.urls import path, include
from questionary import views

urlpatterns = [
    path('',views.main_category, name='category'),
    path('list/<int:pk>/', views.QuestionaryView.as_view(), name='list'),
    path('<int:pk>/', views.detail, name='detail'),
    path('issue/<int:pk>/', views.IssueTracker.as_view(), name='issue'),
    path('issue/<int:pk>/confirm', views.comment_confirm, name='confirm'),
    path('commentDelete/<int:pk>/', views.comment_delete, name='deletion'),

    path('<int:pk>/new/', views.questionary_input, name='questionary_input'),
    path('<int:pk>/update/', views.questionary_update, name='questionary_update'),





]