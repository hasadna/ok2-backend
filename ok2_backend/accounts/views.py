import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from common.utils import create_token
from django.contrib.auth import authenticate


# Create your views here.
@csrf_exempt
def login(request):
    data = json.loads(request.body)
    user = authenticate(username=data['username'], password=data['password'])
    if user:
        token = create_token(user.id)
        return JsonResponse({'token': token})
    return JsonResponse({'error': 'error'})
