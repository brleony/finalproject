from django.shortcuts import render
from django.contrib import messages
from django.db import IntegrityError
from .models import Wallet, Currency, Category, Expense
from django.contrib.auth.models import User

from datetime import datetime

# Create your views here.
def dashboard(request):
    if request.user.is_authenticated:
        return render(request, "dashboard.html", {"title": "Dashboard"})
    else:
        return render(request, "dashboardnotloggedin.html", {"title": "Home"})

def wallets(request):
    if request.method == 'POST':
        name = request.POST["name"]
        code = request.POST["currency"]

        c = Currency.objects.get(code = code)

        # Create new wallet.
        try:
            w = Wallet.objects.create(
                name = name,
                currency = c,
                user = request.user,
            )
            w.save()
            messages.success(request, "You successfully created a new wallet.")
        except IntegrityError:
            messages.error(request, "Your wallet names must be unique.")

    # Query database for wallets.
    wallets = Wallet.objects.filter(user = request.user).values()

    # Change currency_id to unicode html for symbol.
    for wallet in wallets:
        wallet_currency = Currency.objects.filter(pk = wallet["currency_id"]).values()[0]
        wallet["currency_symbol"] = wallet_currency["unicode_html"]

    # Get currencies for form.
    currencies = Currency.objects.all().values()

    return render(request, "wallets.html", {"title": "Wallets", "currencies": currencies, "wallets": wallets})

def createcategory(request):
    if request.method == 'POST':
        name = request.POST["name"]
        color = request.POST["color"]
        wallet_id = request.POST["wallet"]

        w = Wallet.objects.get(id = wallet_id)

        # Save category.
        try:
            c = Category.objects.create(
                    name = name,
                    color = color,
                    wallet = w,
                )
            c.save()
            messages.success(request, "You successfully added a new category.")
        except IntegrityError:
            messages.error(request, "A wallet can't have two categories with the same name.")

    # Wallets for form.
    wallets = Wallet.objects.filter(user = request.user).order_by('-last_used').values()

    # Query database for categories.
    try:
        categories = Category.objects.filter(wallet = wallets[0]["id"]).values()
    except IndexError:
        categories = []

    # List of colors to choose from.
    colors = ['Blue', 'Indigo', 'Purple', 'Pink', 'Red', 'Orange', 'Yellow', 'Green', 'Teal', 'Cyan']

    return render(request, "createcategory.html", {"title": "Categories", "colors": colors, "wallets": wallets, "categories": categories})

def addexpense(request):
    if request.method == 'POST':
        amount = float(request.POST["amount"])
        method = request.POST["method"]
        comment = request.POST["comment"]
        date = datetime.strptime(request.POST["date"], '%m/%d/%Y')
        category_id = request.POST["category"]
        wallet_id = request.POST["wallet"]

        w = Wallet.objects.get(id = wallet_id)
        c = Category.objects.get(id = category_id)

        # Save expense.
        e = Expense.objects.create(
                    amount = amount,
                    method = method,
                    comment = comment,
                    date_spent = date,
                    category = c,
                    wallet = w,
                )
        e.save()
        messages.success(request, "You successfully logged an expense.")

    # Query database for wallets & categories to display in form.
    wallets = Wallet.objects.filter(user = request.user).order_by('-last_used').values()

    try:
        categories = Category.objects.filter(wallet = wallets[0]["id"]).order_by('-last_edited').values()
    except IndexError:
        categories = []

    try:
        recent_expenses = Expense.objects.filter(wallet = wallets[0]["id"]).order_by('-date_created').values()[:5]
    except IndexError:
        recent_expenses = []

    for expense in recent_expenses:
        expense["category"] = Category.objects.filter(pk = expense["category_id"]).values()[0]

    payment_methods = ['Debit', 'Credit', 'Cash', 'Online', 'Paypal', 'Mobile', 'Transfer', 'Cheque', 'Other']

    context = {
        "title": "Log an Expense",
        "wallets": wallets,
        "categories": categories,
        "payment_methods": payment_methods,
        "recent_expenses": recent_expenses
    }

    return render(request, "addexpense.html", context)

def history(request):
    wallets = Wallet.objects.filter(user = request.user).order_by('-last_used').values()
    try:
        expenses = Expense.objects.filter(wallet = wallets[0]["id"]).order_by('-date_spent').values()[:5]
    except IndexError:
        expenses = []

    for expense in expenses:
        expense["category"] = Category.objects.filter(pk = expense["category_id"]).values()[0]

    context = {
        "title": "History",
        "expenses": expenses
    }
    return render(request, "history.html", context)