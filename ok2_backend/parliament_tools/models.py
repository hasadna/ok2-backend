from django.db import models


# Create your models here.
from takanon.models import Takanon


class ParliamentTool(models.Model):
    description = models.TextField()
    takanon = models.ForeignKey(Takanon, on_delete=models.CASCADE)
    # TODO: how to do this? here/another table with more data? calculated or the view?
    # next_date
