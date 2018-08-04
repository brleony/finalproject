from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, "dashboard.html", {"title": "Dashboard"})

def history(request):
    return render(request, "history.html", {"title": "History"})