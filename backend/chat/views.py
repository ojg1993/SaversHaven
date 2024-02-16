from django.shortcuts import render
from chat import views


def index(request):
    return render(request, "chat/index.html")