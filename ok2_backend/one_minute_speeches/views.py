from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View



def one_minute_speeches(request):
    print(request.user)
    return HttpResponse('one minute speech')
