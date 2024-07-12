from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:name>", views.greet, name="greet"),
    path("Zulmira", views.Zulmira, name="Zulmira"),
    path("Januario", views.Januario, name="Januario"),
]
