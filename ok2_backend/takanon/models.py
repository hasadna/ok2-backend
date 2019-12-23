from django.db import models


# Create your models here.
class Section(models.Model):
    name = models.CharField(unique=True)
    ordinal = models.CharField()


class Chapter(models.Model):
    name = models.CharField()
    ordinal = models.CharField()
    section = models.ForeignKey(Section, on_delete=models.CASCADE)


class Clause(models.Model):
    name = models.CharField()
    number = models.IntegerField(db_index=True, unique=True)
    clause = models.TextField()
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL)
    # description = models.TextField()
