from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse


def test_view(request):

    
    return render(request, "hospital/index.html")