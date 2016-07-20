from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting
from.forms import LoginForm

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')

def login(request):
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = LoginForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
			return HttpResponseRedirect('/thanks/')
	    # if a GET (or any other method) we'll create a blank form
		else:
			form = NameForm()
	return render(request, 'name.html', {'form': form})

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

