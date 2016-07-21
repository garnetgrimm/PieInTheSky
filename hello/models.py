from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)

class LoginInfo(models.Model):
	username=models.CharField(max_length=100)
	password=models.CharField(max_length=100)
