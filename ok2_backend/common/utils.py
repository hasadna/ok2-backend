import os

from jose import jwt
from datetime import datetime, timedelta

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 31556952  # year


def get_token(request):
    return jwt.decode(request.headers.get('Authorization'), os.environ['JWT_SECRET'])


def create_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
    return jwt_token
