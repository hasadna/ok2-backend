from django.contrib import admin

# Register your models here.
from .models import Clause


@admin.register(Clause)
class ClauseAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'chapter')

