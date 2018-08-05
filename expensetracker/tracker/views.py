from django.shortcuts import render
from django.contrib import messages

# Create your views here.
def dashboard(request):
    if request.user.is_authenticated:
        return render(request, "dashboard.html", {"title": "Dashboard"})
    else:
        return render(request, "dashboardnotloggedin.html", {"title": "Home"})

def wallets(request):
    return render(request, "wallets.html", {"title": "My Wallets"})

def createcategory(request):
    # List of colors to choose from.
    colors = ['Blue', 'Indigo', 'Purple', 'Pink', 'Red', 'Orange', 'Yellow', 'Green', 'Teal', 'Cyan']
    return render(request, "createcategory.html", {"title": "Create New Category", "colors": colors})

def addexpense(request):
    return render(request, "addexpense.html", {"title": "Log an Expense"})

def history(request):
    return render(request, "history.html", {"title": "History"})