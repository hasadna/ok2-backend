from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View



def check(request):
    print(request.user)
    return HttpResponse('it works')
