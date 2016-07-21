from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token

from .models import Greeting, LoginInfo
from.forms import LoginForm

# Create your views here.
def index(request):
	return render(request, 'index.html')
	
@csrf_exempt
@requires_csrf_token
def login(request):
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = LoginForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
			newUsername = form.cleaned_data['username']
			newPassword = form.cleaned_data['password']
			
			info = LoginInfo(username=newUsername, password=newPassword)
			info.save()
			
			username.save()
			
			return HttpResponse('Hello ' + username)
	    # if a GET (or any other method) we'll create a blank form
		else:
			form = LoginForm()
			return HttpResponse('Hello world')
	return render(request, 'name.html', {'form': form})

def db(request):
	
	greeting = Greeting()
	greeting.save()
	
	greetings = Greeting.objects.all()
	
	return render(request, 'db.html', {'greetings': greetings})

