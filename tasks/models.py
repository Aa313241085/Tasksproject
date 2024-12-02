from django.db import models
from django.forms import ModelForm


class User(models.Model):
    id = models.IntegerField(primary_key = True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    is_admin = models.BooleanField(default=False)


class Task(models.Model):

    class Category(models.TextChoices):
        Import = 'Import'
        Eport = 'Export'
        Server = 'Server'
        Bookkeeping = 'Bookkeeping'

    class Client(models.TextChoices):
        United = 'United'
        Sky = 'Sky'
        WorldCourier = 'World Courier'
        Krief = 'Krief'

    id = models.IntegerField(primary_key = True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    client = models.CharField(max_length=15, choices=Client.choices)
    create_date = models.DateField(auto_now=True)
    category = models.CharField(max_length=30, choices=Category.choices)
    description = models.CharField(max_length=256)

class SharedTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ["client", "category", "description"]