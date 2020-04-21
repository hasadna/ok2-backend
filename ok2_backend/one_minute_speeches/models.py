from django.contrib.auth import get_user_model as user_model
from django.db import models

User = user_model()
# Create your models here.


class Speech(models.Model):
    title = models.TextField()
    # max 1 minute speech, should see how to validate
    speech = models.TextField()
    parliament_member_speech = models.ManyToManyField(User)
