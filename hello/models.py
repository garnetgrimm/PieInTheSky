from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)

class LoginInfo(models.Model):
	username=models.TextField()
	password=models.TextField()
	
	def __str__(self):
		return self.username