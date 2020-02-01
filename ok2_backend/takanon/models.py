from django.db import models


class Section(models.Model):
    ordinal = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.ordinal}: {self.name}"


class Chapter(models.Model):
    ordinal = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=100)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ordinal}: {self.name}"


class Clause(models.Model):
    name = models.CharField(max_length=200)
    number = models.CharField(max_length=10, db_index=True, unique=True)
    clause_text = models.TextField()
    chapter = models.ForeignKey(Chapter, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.number}: {self.name}"