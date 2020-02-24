import os
from datetime import datetime, timedelta
import jwt

from django.contrib.sessions.backends.signed_cookies import SessionStore

JWT_USER_FIELDS = ['email', 'slug']


class SessionStore(SessionStore):
    def load(self):
        try:
            return jwt.decode(self.session_key[2:-1], os.environ['JWT_SECRET'], algorithms=['HS256'])
        except Exception as ex:
            print(ex)
            self.create()
        return {}

    def _get_session_key(self):
        session_cache = getattr(self, '_session_cache', {})
        return jwt.encode({
            **session_cache,
            'exp': datetime.utcnow() + timedelta(days=30)
        }, os.environ['JWT_SECRET'])
