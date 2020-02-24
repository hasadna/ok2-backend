from django.http import HttpResponse
from django.shortcuts import render


def check(request):
    print(request.user)
    return HttpResponse('it works')
