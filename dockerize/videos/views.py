from os import name
from django.shortcuts import render, HttpResponse
from django.views.generic import ListView
from .models import *


def check(request):
    cat = Category.objects.get(name='sport')
    return HttpResponse(cat)
