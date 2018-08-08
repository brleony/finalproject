from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import IntegrityError

def login_view(request):
    if request.user.is_authenticated:
        return render(request, "dashboard.html", {"title": "Dashboard"})
    elif request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in.')
            return redirect('/tracker/dashboard')
        else:
            messages.error(request, 'Invalid credentials.')
            return render(request, "users/login.html", {"title": "Log In"})
    else:
        return render(request, "users/login.html", {"title": "Log In"})

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out.')
    return redirect('/tracker/dashboard')

def register(request):
    # If user is logged in, direct to index.
    if request.user.is_authenticated:
        return render(request, "dashboard.html", {"title": "Dashboard"})
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
            messages.error(request, 'Must provide a username.')
            return render(request, "users/register.html", {"title": "Register"})
        elif 20 < len(username):
            messages.error(request, 'Username can not be longer than 20 characters.')
            return render(request, "users/register.html", {"title": "Register"})
        elif len(username) < 4:
            messages.error(request, 'Username must be longer than 4 characters.')
            return render(request, "users/register.html", {"title": "Register"})

        # Validate first name.
        if not firstname:
            messages.error(request, 'Must provide a first name.')
            return render(request, "users/register.html", {"title": "Register"})
        elif 100 < len(firstname):
            messages.error(request, 'First name can not be longer than 100 characters.')
            return render(request, "users/register.html", {"title": "Register"})

        # Validate last name.
        if not lastname:
            messages.error(request, 'Must provide a last name.')
            return render(request, "users/register.html", {"title": "Register"})
        elif 100 < len(lastname):
            messages.error(request, 'Last name can not be longer than 100 characters.')
            return render(request, "users/register.html", {"title": "Register"})

        # Validate email address.
        try:
            validate_email(email)
        except ValidationError as error:
            messages.error(request, error)
            return render(request, "users/register.html", {"title": "Register"})

        # Validate password.
        if not password1:
            messages.error(request, 'Must provide a password.')
            return render(request, "users/register.html", {"title": "Register"})
        try:
            validate_password(password1)
        except ValidationError as error:
            messages.error(request, error)
            return render(request, "users/register.html", {"title": "Register"})

        # Ensure password and confirmation password are the same.
        if password1 != password2:
            messages.error(request, "Passwords don't match.")
            return render(request, "users/register.html", {"title": "Register"})

        # Create and save user.
        try:
            user = User.objects.create_user(username, email, password1)
            user.first_name = firstname
            user.last_name = lastname
            user.save()
        except IntegrityError:
            messages.error(request, 'Username already taken.')
            return render(request, "users/register.html", {"title": "Register"})

        # Log user in.
        login(request, user)
        messages.error(request, f"Welcome, {firstname}!")
        return render(request, "dashboard.html", {"title": "Dashboard"})

    # If method is 'GET' (or any other)
    else:
        return render(request, "users/register.html", {"title": "Register"})