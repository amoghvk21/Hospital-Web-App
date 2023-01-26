from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django import forms
from predict import predict
from PIL import Image
from django.forms.widgets import NumberInput


def index_view(request):
    
    # Redirect to login
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    # Redirect to patient homepage
    if request.user.role == 'p':
        return HttpResponseRedirect(reverse("patient", kwargs={'id': request.user.id}))
    else:
        # Redirect to doctor homepage
        return HttpResponseRedirect(reverse("doctor"))


class RegisterForm(forms.Form):

    SEX = [
        ('m', 'Male'), 
        ('f', 'Female')
    ]

    ROLES = [
        ('p', 'Patient'),
        ('d', 'Doctor')
    ]

    name = forms.CharField(max_length=50, required=True)
    surname = forms.CharField(max_length=50, required=True)
    dob = forms.DateField(required=True, label='Date of Birth', widget=NumberInput(attrs={'type': 'date'}))
    sex = forms.CharField(widget=forms.Select(choices=SEX), required=True)
    email = forms.EmailField(max_length=50, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    role = forms.CharField(widget=forms.Select(choices=ROLES), max_length=50, required=True)

# dob = datetime.strptime(form.cleaned_data['dob'], '%Y-%m-%d').date()

def register_view(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    else:
        if request.method == 'POST':
            # Get data
            form = RegisterForm(request.POST)

            # Input validation
            if form.is_valid():

                # Extract each field
                name = form.cleaned_data['name']
                surname = form.cleaned_data['surname']
                dob = form.cleaned_data['dob']
                sex = form.cleaned_data['sex']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                role = form.cleaned_data['role']

                # Check if user already exists
                try:
                    user = User.objects.get(email=email)
                    return render(request, "hospital/register.html", {
                        "message": "Error, email already taken",
                        'form': RegisterForm(auto_id='register_%s')
                    })
                except:
                    pass 

                # Create new user
                try:
                    user = User(first_name=name, last_name=surname, dob=dob, sex=sex, email=email, password=password, role=role, username=email)
                    user.save()
                except:
                    return render(request, "hospital/register.html", {
                        "message": "Error",
                        'form': RegisterForm(auto_id='register_%s')
                    })

                # Login to this user
                login(request, user)

                # Redirect user
                return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, 'hospital/register.html', {
                'form': RegisterForm(auto_id='register_%s')
            })


'''
def register_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    else:

        if request.method == "POST":

            # Get data
            name = request.POST["name"]
            surname = request.POST["surname"]
            dob = datetime.strptime(request.POST["dob"], '%Y-%m-%d').date()
            sex = request.POST["sex"]
            email = request.POST["email"]
            password = request.POST["password"]
            role = request.POST["role"]

            # Check if user already exists
            try:
                user = User.objects.get(email=email)
                return render(request, "hospital/register.html", {
                    "message": "Error, email already taken"
                })
            except:
                pass 

            # Create new user
            try:
                user = User(first_name=name, last_name=surname, dob=dob, sex=sex, email=email, password=password, role=role, username=email)
                user.save()
            except:
                return render(request, "hospital/register.html", {
                    "message": "Error"
                })

            # Login to this user
            login(request, user)

            # Redirect user
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "hospital/register.html")
'''


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    else:

        if request.method == "POST":

            # Get data
            email = request.POST["email"]
            password = request.POST["password"]

            # Find the user
            try:
                user = User.objects.get(email=email)
            except:
                return render(request, "hospital/login.html", {
                    "message": "User doesn't exist"
                })
            
            # Check the password
            if user.password != password:
                return render(request, "hospital/login.html", {
                    "message": "Incorrect password"
                })
            else:
                # Login
                login(request, user)

                # Redirect user
                return HttpResponseRedirect(reverse("index"))

        return render(request, "hospital/login.html")


def logout_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    else:
        logout(request)
        return HttpResponseRedirect(reverse("index"))


def patient_homepage_view(request, id):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    elif ((request.user.id == id) or (request.user.role == 'd')):
        return render(request, "hospital/patient.html", {
            'patient': User.objects.get(id=id)
        })

    else:
        return HttpResponseRedirect(reverse("index"))


def doctor_homepage_view(request):

    if request.user.role == 'd':
        return render(request, "hospital/doctor.html", {
            'patients': User.objects.filter(treatedBy=request.user.id)
        })
    else:
        return HttpResponseRedirect(reverse("index"))


class ImageForm(forms.Form):
    history = forms.CharField(label='', widget=forms.Textarea())
    img = forms.ImageField(required=False, label='')


def edit_view(request, id):
    
    # Check if they have access
    if request.user.role == 'd':

        if request.method == 'POST':
            form = ImageForm(request.POST, request.FILES)
            if form.is_valid():

                # Get the form data
                history = form.cleaned_data.get('history')
                img = form.cleaned_data.get('img')

                # Find and update fields
                user = User.objects.get(id=id)
                user.history = history
                user.img = img
                user.save()

                # Get diagnosis from neural net
                img = Image.open(f'hospital/static/hospital/img/{id}.png')
                diagnosis = predict(img)

                # Save new diagnois
                user.diagnosis = diagnosis
                user.save()

                # Redirect user back to patient page
                return HttpResponseRedirect(reverse('patient', kwargs={'id': id}))
        else:
            return render(request, "hospital/edit.html", {
                'patient': User.objects.get(id=id),
                'form': ImageForm(initial={
                    'history': User.objects.get(id=id).history
                })
            })
    else:
        return HttpResponseRedirect(reverse('index'))