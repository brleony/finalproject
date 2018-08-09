from django.shortcuts import render
from django.contrib import messages
from django.db import IntegrityError
from .models import Wallet, Currency, Category, Expense
from django.contrib.auth.models import User
from datetime import datetime

from tracker.helpers import getexpensedetails

# Create your views here.
def dashboard(request):
    if request.user.is_authenticated:
        # Query database for 10 most recent expenses.
        try:
            expenses = Expense.objects.filter(created_by = request.user,).order_by('-date_created').values()
        except IndexError:
            expenses = []

        # Query database for categories and wallets and currencies used in recent expenses.
        expenses = getexpensedetails(expenses, Category, 'category_id', 'category', None)
        expenses = getexpensedetails(expenses, Wallet, 'wallet_id', 'wallet', None)
        expenses = getexpensedetails(expenses, Currency, 'wallet', 'currency', 'currency_id')

        # Save last 10 expenses.
        recent_expenses = expenses[:10]

        # Counter.
        expenses_this_month = 0
        amount_this_month = 0
        expenses_all_time = 0
        amount_all_time = 0

        # Count expenses in current month and all time.
        for expense in expenses:
            # If month and year are current month and year.
            if expense["date_spent"].month == datetime.today().month and expense["date_spent"].year == datetime.today().year:
                expenses_this_month += 1
                amount_this_month += expense["amount"]

            expenses_all_time += 1
            amount_all_time += expense["amount"]

        context = {
            "title": "Dashboard",
            "recent_expenses": recent_expenses,
            "expenses_this_month": expenses_this_month,
            "expenses_all_time": expenses_all_time,
            "amount_this_month": amount_this_month,
            "amount_all_time": amount_all_time,
        }

        return render(request, "dashboard.html", context)
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
        categories = Category.objects.filter(wallet__user = request.user).values()
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

        # Validate category name.
        if not name:
            messages.error(request, 'Must provide a name.')
            return render(request, "createcategory.html", context)
        elif 20 < len(name):
            messages.error(request, 'Name can not be longer than 20 characters.')
            return render(request, "createcategory.html", context)
        elif len(name) < 3:
            messages.error(request, 'Name must be longer than 3 characters.')
            return render(request, "createcategory.html", context)

        # Check if a color and wallet were chosen.
        if not color:
            messages.error(request, 'Must choose a color.')
            return render(request, "createcategory.html", context)
        if not wallet_id:
            messages.error(request, 'Must choose a wallet.')
            return render(request, "createcategory.html", context)

        # Try to get wallet object.
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
                    created_by = request.user,
                )
            c.save()
            messages.success(request, "You successfully added a new category.")
        except IntegrityError:
            messages.error(request, "A wallet can't have two categories with the same name.")

    return render(request, "createcategory.html", context)

def addexpense(request):
    # Query database for wallets to show in form.
    wallets = Wallet.objects.filter(user = request.user).order_by('-last_used').values()

    # Query database for categories to show in form.
    try:
        categories = Category.objects.filter(wallet = wallets[0]["id"]).order_by('-last_edited').values()
    except IndexError:
        categories = []

    # Query database for 5 most recent expenses.
    try:
        recent_expenses = Expense.objects.filter(created_by = request.user,).order_by('-date_created').values()[:5]
    except IndexError:
        recent_expenses = []

    # Query database for categories and wallets and currencies used in recent expenses.
    recent_expenses = getexpensedetails(recent_expenses, Category, 'category_id', 'category', None)
    recent_expenses = getexpensedetails(recent_expenses, Wallet, 'wallet_id', 'wallet', None)
    recent_expenses = getexpensedetails(recent_expenses, Currency, 'wallet', 'currency', 'currency_id')

    payment_methods = ['Debit', 'Credit', 'Cash', 'Online', 'Paypal', 'Mobile', 'Transfer', 'Cheque', 'Other']

    context = {
        "title": "Log an Expense",
        "wallets": wallets,
        "categories": categories,
        "payment_methods": payment_methods,
        "recent_expenses": recent_expenses
    }

    if request.method == 'POST':
        # Try to convert amount to float.
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

        # Check if payment method and wallet were chosen.
        if not wallet_id:
            messages.error(request, 'Must choose a wallet')
            return render(request, "addexpense.html", context)
        if not method:
            messages.error(request, 'Must choose a method.')
            return render(request, "addexpense.html", context)

        # Validate comment length.
        if 255 < len(comment):
            messages.error(request, 'Comment can not be longer than 255 characters.')
            return render(request, "addexpense.html", context)

        # Try to get wallet object.
        try:
            w = Wallet.objects.filter(user = request.user).filter(id = wallet_id)[0]
        except IndexError:
            messages.error(request, 'We could not find that wallet.')
            return render(request, "addexpense.html", context)

        # If category was chosen, get category object.
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
                    created_by = request.user,
                )
        if c:
            e.category = c
        e.save()
        messages.success(request, "You successfully logged an expense.")

    return render(request, "addexpense.html", context)

def history(request):
    try:
        expenses = Expense.objects.filter(wallet__user = request.user).order_by('-date_spent').values()
    except IndexError:
        expenses = []

    expenses = getexpensedetails(expenses, Category, 'category_id', 'category', None)
    expenses = getexpensedetails(expenses, Wallet, 'wallet_id', 'wallet', None)
    expenses = getexpensedetails(expenses, Currency, 'wallet', 'currency', 'currency_id')

    print(expenses)

    context = {
        "title": "History",
        "expenses": expenses
    }
    return render(request, "history.html", context)