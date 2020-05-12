import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, password_validation

from common.utils import create_token
from accounts.models import OkUser
from accounts.serializers import RegistrationSerializer


# Create your views here.
@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = authenticate(
            email=data['email'], password=data['password'])
        if user:
            token = create_token(user.id)
            return JsonResponse(user.getUserResponse(token))
        return JsonResponse({'error': 'wrong email or password'}, status=401)


@csrf_exempt
def registration_view(request):
    if request.method == 'POST':
        res = {}
        data = json.loads(request.body)
        email = data['email'].lower()
        password = data['password']
        if validate_email(email) != None:
            res['error_message'] = 'This email is already in use.'
            res['response'] = 'Error'
            return JsonResponse(res, status=400)
        passValid = validate_password(password)
        if passValid != None:
            res['error_message'] = passValid
            res['response'] = 'Error'
            return JsonResponse(res, status=400)

        serializer = RegistrationSerializer(data=data)

        if serializer.is_valid():
            user = serializer.save()
            token = create_token(user.id)
            return JsonResponse(user.getUserResponse(token), status=201)
        else:
            error = serializer.errors
        return JsonResponse(error, status=400)


def validate_email(email):
    user = None
    try:
        user = OkUser.objects.get(email=email)
    except OkUser.DoesNotExist:
        return None
    if user != None:
        return email


def validate_password(value):
    isValid = password_validation.validate_password(value)
    return isValid
