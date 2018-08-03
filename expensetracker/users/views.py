from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

def login_view(request):
    if request.user.is_authenticated:
        return render(request, "index.html")
    elif request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return render(request, "index.html", {"message": "You are logged in."})
        else:
            return render(request, "users/login.html", {"message": "Invalid credentials."})
    else:
        return render(request, "users/login.html", {"message": None})

def logout_view(request):
    logout(request)
    return render(request, "index.html", {"message": "Logged out."})

def register(request):
    # If user is logged in, direct to index.
    if request.user.is_authenticated:
        return render(request, "index.html")
    # If form was submitted.
    elif request.method == 'POST':
        # Save fields.
        username = request.POST["username"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        # Validate username.
        if not username:
            return render(request, "users/register.html", {"message": "Must provide a username."})
        elif 20 < len(username):
            return render(request, "users/register.html", {"message": "Username can not be longer than 20 characters."})
        elif len(username) < 4:
            return render(request, "users/register.html", {"message": "Username must be longer than 4 characters."})

        # Validate first name.
        if not firstname:
            return render(request, "users/register.html", {"message": "Must provide a first name."})
        elif 100 < len(firstname):
            return render(request, "users/register.html", {"message": "First name can not be longer than 100 characters."})

        # Validate last name.
        if not lastname:
            return render(request, "users/register.html", {"message": "Must provide a last name."})
        elif 100 < len(lastname):
            return render(request, "users/register.html", {"message": "Last name can not be longer than 100 characters."})

        # Validate email address.
        try:
            validate_email(email)
        except ValidationError as error:
            return render(request, "users/register.html", {"message": error})

        # Validate password.
        if not password1:
            return render(request, "users/register.html", {"message": "Must provide a password."})
        try:
            validate_password(password1)
        except ValidationError as error:
            return render(request, "users/register.html", {"message": error})

        # Ensure password and confirmation password are the same.
        if password1 != password2:
            return render(request, "users/register.html", {"message": "Passwords don't match."})

        # Create and save user.
        user = User.objects.create_user(username, email, password1)
        user.first_name = firstname
        user.last_name = lastname
        user.save()

        # Log user in.
        login(request, user)
        return render(request, "index.html", {"message": f"Welcome, {firstname}!"})
    # If method is 'GET' (or any other)
    else:
        return render(request, "users/register.html")