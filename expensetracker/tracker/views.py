from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, "dashboard.html", {"title": "Dashboard"})

def createcategory(request):
    return render(request, "createcategory.html", {"title": "Create New Category"})

def addexpense(request):
    return render(request, "addexpense.html", {"title": "Log an Expense"})

def history(request):
    return render(request, "history.html", {"title": "History"})