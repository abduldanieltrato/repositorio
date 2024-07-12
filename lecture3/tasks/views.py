from django.http import HttpResponse
from django.shortcuts import render

tasks: list[str] = ["foo", "bar", "baz"]

# Create your views here.
def index(request) -> HttpResponse:
    return render(request=request, template_name="tasks/index.html", context={
        "tasks": tasks
    })
