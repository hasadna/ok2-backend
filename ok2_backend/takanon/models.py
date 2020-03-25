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
    chapter = models.ForeignKey(Chapter, null=True, on_delete=models.SET_NULL)
    latest_version = models.CharField(max_length=30, null=True)

    def __str__(self):
        return f"{self.number}: {self.name}"


class ClauseVersion(models.Model):
    clause = models.ForeignKey(Clause, on_delete=models.CASCADE)
    version = models.CharField(max_length=30)
    version_text = models.TextField()

    class Meta:
        unique_together = [('clause', 'version')]

    def __str__(self):
        return f"Clause {self.clause} version {self.version}"
