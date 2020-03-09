import os

from jose import jwt


def get_token(request):
    return jwt.decode(request.headers.get('Authorization'), os.environ['JWT_SECRET'])


def create_token(user_id):
    res = jwt.encode({'user_id': user_id}, os.environ['JWT_SECRET'], algorithm='HS256')
    return res
