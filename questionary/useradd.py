import django.contrib.auth
from django.contrib.auth.models import User


User = django.contrib.auth.get_user_model()
user = User.objects.create_user('help8', password='eksql12#')
user.save()
