from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "index.html", {"title": "Dashboard"})

def history(request):
    return render(request, "history.html", {"title": "History"})