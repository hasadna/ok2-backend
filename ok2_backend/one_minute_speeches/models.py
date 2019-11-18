from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Speech(models.Model):
    title = models.TextField()
    # max 1 minute speech, should see how to validate
    speech = models.TextField()
    parliament_member_speech = models.ManyToManyField(User)
