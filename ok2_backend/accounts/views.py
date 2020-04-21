import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from common.utils import create_token
from django.contrib.auth import authenticate
from accounts.models import OkUser


# Create your views here.
@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = authenticate(
            username=data['username'], password=data['password'])
        if user:
            token = create_token(user.id)
            return JsonResponse({'token': token,
                                 'username': user.username,
                                 'firstName': user.first_name,
                                 'lastName': user.last_name,
                                 'email': user.email,
                                 'isActive': user.is_active,
                                 })
        return JsonResponse({'error': 'wrong email or password'}, status=401)


@csrf_exempt
def registration_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # return JsonResponse(data)
        email = data.email.lower()
        if validate_email(email) != None:
            data['error_message'] = 'That email is already in use.'
            data['response'] = 'Error'
            return JsonResponse(data)

        serializer = RegistrationSerializer(json_data)

        if serializer.is_valid():
            user = serializer.save()
            token = create_token(user.id)
            return JsonResponse({'token': token,
                                 'username': user.username,
                                 'firstName': user.first_name,
                                 'lastName': user.last_name,
                                 'email': user.email,
                                 'isActive': user.is_active,
                                 }, status=status.HTTP_201_CREATED)
        else:
            error = serializer.errors
        return JsonResponse(error, status=status.HTTP_400_BAD_REQUEST)


def validate_email(email):
    user = None
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return None
    if user != None:
        return email
