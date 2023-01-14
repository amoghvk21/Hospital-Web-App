from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from datetime import datetime


def test_view(request):
    return render(request, "hospital/index.html")


def register_view(request):
    if request.method == "POST":

        # Get data
        name = request.POST["name"]
        surname = request.POST["surname"]
        dob = datetime.strptime(request.POST["dob"], '%Y-%m-%d').date()
        sex = request.POST["sex"]
        email = request.POST["email"]
        password = request.POST["password"]
        role = request.POST["role"]

        # Create new user
        try:
            user = User(first_name=name, last_name=surname, dob=dob, sex=sex, email=email, password=password, role=role)
            user.save()
        except:
            return render(request, "hospital/register.html", {
                "message": "Error, User already exists"
            })

        # Login to this user
        login(request, user)

        # Redirect user
        return HttpResponseRedirect(reverse("test"))
    else:
        return render(request, "hospital/register.html")


def login_view(request):
    if request.method == "POST":

        # Get data
        email = request.POST["email"]
        password = request.POST["password"]

        # Find the user
        try:
            user = User.objects.get(email=email)
        except:
            return render(request, "hospital/register.html", {
                "message": "User doesn't exist"
            })
        
        # Check the password
        if user.password != password:
            return render(request, "hospital/register.html", {
                "message": "Incorrect password"
            })
        else:
            # Login
            login(request, user)

            # Redirect user
            return HttpResponseRedirect(reverse("test"))

    return render(request, "hospital/login.html")