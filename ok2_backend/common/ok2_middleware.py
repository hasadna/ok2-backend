import os

from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import User, AnonymousUser

import jwt


def get_token(request):
    if 'authentication' in request.headers:
        return jwt.decode(request.headers['authentication'], os.environ['JWT_SECRET'])


def get_user(request):
    token = get_token(request)
    if token:
        return User.objects.get(pk=token['user_id'])
    return AnonymousUser()


class OkMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        # do the job of working with jwt, happens before the view is called
        # request.user = get_user(request)

        response = self.get_response(request)
        if request.user.is_anonymous:
            return response

        for field in ['id', 'username', 'email']:
            if field not in request.session:
                request.session[field] = getattr(request.user, field)

        # do the job after the view is called if relevant
        return response
