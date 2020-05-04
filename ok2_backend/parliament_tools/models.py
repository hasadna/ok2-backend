from django.db import models

from takanon.models import Clause

# Create your models here.

class ParliamentTool(models.Model):
    description = models.TextField()
    # TODO: A tool relates to a (non continous) range of rulebook cluases
    # takanon = models.ForeignKey(Clause, null=True, on_delete=models.SET_NULL)
    # TODO: how to do this? here/another table with more data? calculated or the view?
    # next_date
