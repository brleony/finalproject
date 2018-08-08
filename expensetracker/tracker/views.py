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
    # Query database for wallets.
    wallets = Wallet.objects.filter(user = request.user).values()

    # Change currency_id to unicode html for symbol.
    for wallet in wallets:
        wallet_currency = Currency.objects.filter(pk = wallet["currency_id"]).values()[0]
        wallet["currency_symbol"] = wallet_currency["unicode_html"]

    # Get currencies for form.
    currencies = Currency.objects.all().values

    context = {
        "title": "Wallets",
        "currencies": currencies,
        "wallets": wallets
    }

    if request.method == 'POST':
        name = request.POST["name"]
        code = request.POST["currency"]

        if not name:
            messages.error(request, 'Must provide a name.')
            return render(request, "wallets.html", context)
        elif 20 < len(name):
            messages.error(request, 'Name can not be longer than 20 characters.')
            return render(request, "wallets.html", context)
        elif len(name) < 3:
            messages.error(request, 'Name must be longer than 3 characters.')
            return render(request, "wallets.html", context)

        if not code:
            messages.error(request, 'Must choose a currency.')
            return render(request, "wallets.html", context)

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

    return render(request, "wallets.html", context)

def createcategory(request):
    # Wallets for form.
    wallets = Wallet.objects.filter(user = request.user).order_by('-last_used').values()

    # Query database for categories.
    try:
        categories = Category.objects.filter(wallet = wallets[0]["id"]).values()
    except IndexError:
        categories = []

    # List of colors to choose from.
    colors = ['Blue', 'Indigo', 'Purple', 'Pink', 'Red', 'Orange', 'Yellow', 'Green', 'Teal', 'Cyan']

    context = {
        "title": "Categories",
        "colors": colors,
        "wallets": wallets,
        "categories": categories
    }

    if request.method == 'POST':
        name = request.POST["name"]
        color = request.POST["color"]
        wallet_id = request.POST["wallet"]

        if not name:
            messages.error(request, 'Must provide a name.')
            return render(request, "createcategory.html", context)
        elif 20 < len(name):
            messages.error(request, 'Name can not be longer than 20 characters.')
            return render(request, "createcategory.html", context)
        elif len(name) < 3:
            messages.error(request, 'Name must be longer than 3 characters.')
            return render(request, "createcategory.html", context)

        if not color:
            messages.error(request, 'Must choose a color.')
            return render(request, "createcategory.html", context)
        if not wallet_id:
            messages.error(request, 'Must choose a wallet.')
            return render(request, "createcategory.html", context)

        try:
            w = Wallet.objects.filter(user = request.user).filter(id = wallet_id)[0]
        except IndexError:
            messages.error(request, 'We could not find that wallet.')
            return render(request, "createcategory.html", context)

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

    return render(request, "createcategory.html", context)

def addexpense(request):
    # Query database for wallets.
    wallets = Wallet.objects.filter(user = request.user).order_by('-last_used').values()

    # Query database for categories.
    try:
        categories = Category.objects.filter(wallet = wallets[0]["id"]).order_by('-last_edited').values()
    except IndexError:
        categories = []

    # Query database for 5 most recent expenses.
    try:
        recent_expenses = Expense.objects.filter(wallet = wallets[0]["id"]).order_by('-date_created').values()[:5]
    except IndexError:
        recent_expenses = []

    # Query database for categories used in recent expenses.
    for expense in recent_expenses:
        if expense["category_id"]:
            expense["category"] = Category.objects.filter(pk = expense["category_id"]).values()[0]
        else:
            expense["category"] = ""

    payment_methods = ['Debit', 'Credit', 'Cash', 'Online', 'Paypal', 'Mobile', 'Transfer', 'Cheque', 'Other']

    context = {
        "title": "Log an Expense",
        "wallets": wallets,
        "categories": categories,
        "payment_methods": payment_methods,
        "recent_expenses": recent_expenses
    }

    if request.method == 'POST':
        try:
            amount = float(request.POST["amount"])
        except ValueError:
            messages.error(request, 'Enter an amount in numbers.')
            return render(request, "addexpense.html", context)

        try:
            date = datetime.strptime(request.POST["date"], '%m/%d/%Y')
        except ValueError:
            messages.error(request, 'Enter a date like this: mm/dd/yy.')
            return render(request, "addexpense.html", context)

        method = request.POST["method"]
        comment = request.POST["comment"]
        category_id = request.POST["category"]
        wallet_id = request.POST["wallet"]

        if not wallet_id:
            messages.error(request, 'Must choose a wallet')
            return render(request, "addexpense.html", context)

        if not method:
            messages.error(request, 'Must choose a method.')
            return render(request, "addexpense.html", context)

        if 255 < len(comment):
            messages.error(request, 'Comment can not be longer than 255 characters.')
            return render(request, "addexpense.html", context)

        try:
            w = Wallet.objects.filter(user = request.user).filter(id = wallet_id)[0]
        except IndexError:
            messages.error(request, 'We could not find that wallet.')
            return render(request, "addexpense.html", context)

        if category_id:
            try:
                c = Category.objects.filter(id = category_id)[0]
            except IndexError:
                c = None
                messages.error(request, 'We could not find that category.')
                return render(request, "addexpense.html", context)
        else:
            c = None

        # Save expense.
        e = Expense.objects.create(
                    amount = amount,
                    method = method,
                    comment = comment,
                    date_spent = date,
                    wallet = w,
                )
        if c:
            e.category = c
        e.save()
        messages.success(request, "You successfully logged an expense.")

    return render(request, "addexpense.html", context)

def history(request):
    wallets = Wallet.objects.filter(user = request.user).order_by('-last_used').values()

    try:
        expenses = Expense.objects.filter(wallet = wallets[0]["id"]).order_by('-date_spent').values()
    except IndexError:
        expenses = []

    for expense in expenses:
        if expense["category_id"]:
            expense["category"] = Category.objects.filter(pk = expense["category_id"]).values()[0]
        else:
            expense["category"] = ""

    context = {
        "title": "History",
        "expenses": expenses
    }
    return render(request, "history.html", context)