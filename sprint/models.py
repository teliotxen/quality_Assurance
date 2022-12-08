from django.db import models

# Create your models here.


class TestSet(models.Model):
    title = models.CharField(max_length=50)
    contents = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title





class Task(models.Model):
    set = models.ForeignKey('Scenario', on_delete=models.CASCADE)
    test_set = models.ForeignKey('TestSet', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=20)
    contents = models.TextField()
    start_date = models.DateField(null=True)
    due_date = models.DateField(null=True)
    charge = models.ForeignKey('info.DevTeam', on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.title


class Scenario(models.Model):
    set = models.ForeignKey('TestSet', on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    contents = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    tasks = models.ManyToManyField(Task)

    def __str__(self):
        return self.title







