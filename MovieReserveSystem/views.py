from django.shortcuts import render
from django.http import HttpResponse

from .models import Movie

# Create your views here.


def index(request):
    return HttpResponse("Welcome to the site!")

def index_template(request):
    movies = Movie.objects.all()
    print(movies)
    context = {
        'movies': movies,
    }
    return render(request, 'index.html', context)

def hello(request):
    return HttpResponse("Hello there!")


def signup_view(request):
    pass

def login_view(request):
    pass

def logout_view(request):
    pass

def user_view(request):
    pass

def other_view(request):
    pass
