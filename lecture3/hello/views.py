from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request) -> HttpResponse:
    return render(request=request, template_name="hello/index.html")

def greet(request, name) -> HttpResponse:
    return render(request, "hello/greet.html", {
        "name": name.capitalize()
    })

def Januario(request) -> HttpResponse:
    return HttpResponse(content="Hello, Januario!")

def Zulmira(request) -> HttpResponse:
    return HttpResponse(content="Hello, Zulmira!")
