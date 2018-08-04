from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import IntegrityError

def login_view(request):
    if request.user.is_authenticated:
        return render(request, "index.html", {"title": "Dashboard"})
    elif request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return render(request, "index.html", {"message": "You are logged in.", "title": "Dashboard"})
        else:
            return render(request, "users/login.html", {"message": "Invalid credentials.", "title": "Log In"})
    else:
        return render(request, "users/login.html", {"message": None, "title": "Log In"})

def logout_view(request):
    logout(request)
    return render(request, "index.html", {"message": "Logged out.", "title": "Dashboard"})

def register(request):
    # If user is logged in, direct to index.
    if request.user.is_authenticated:
        return render(request, "index.html", {"title": "Dashboard"})
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
            return render(request, "users/register.html", {"message": "Must provide a username.", "title": "Register"})
        elif 20 < len(username):
            return render(request, "users/register.html", {"message": "Username can not be longer than 20 characters.", "title": "Register"})
        elif len(username) < 4:
            return render(request, "users/register.html", {"message": "Username must be longer than 4 characters.", "title": "Register"})

        # Validate first name.
        if not firstname:
            return render(request, "users/register.html", {"message": "Must provide a first name.", "title": "Register"})
        elif 100 < len(firstname):
            return render(request, "users/register.html", {"message": "First name can not be longer than 100 characters.", "title": "Register"})

        # Validate last name.
        if not lastname:
            return render(request, "users/register.html", {"message": "Must provide a last name.", "title": "Register"})
        elif 100 < len(lastname):
            return render(request, "users/register.html", {"message": "Last name can not be longer than 100 characters.", "title": "Register"})

        # Validate email address.
        try:
            validate_email(email)
        except ValidationError as error:
            return render(request, "users/register.html", {"message": error, "title": "Register"})

        # Validate password.
        if not password1:
            return render(request, "users/register.html", {"message": "Must provide a password.", "title": "Register"})
        try:
            validate_password(password1)
        except ValidationError as error:
            return render(request, "users/register.html", {"message": error, "title": "Register"})

        # Ensure password and confirmation password are the same.
        if password1 != password2:
            return render(request, "users/register.html", {"message": "Passwords don't match.", "title": "Register"})

        # Create and save user.
        try:
            user = User.objects.create_user(username, email, password1)
            user.first_name = firstname
            user.last_name = lastname
            user.save()
        except IntegrityError:
            return render(request, "users/register.html", {"message": "Username must be unique.", "title": "Register"})

        # Log user in.
        login(request, user)
        return render(request, "index.html", {"message": f"Welcome, {firstname}!", "title": "Dashboard"})

    # If method is 'GET' (or any other)
    else:
        return render(request, "users/register.html", {"title": "Register"})