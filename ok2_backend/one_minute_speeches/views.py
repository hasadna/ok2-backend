from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import View


# Create your views here.
class Tool(View):
    def get(self, requrest):
        return JsonResponse({
            'key': 'val'
        })


def func(request):
    return 'hello'
