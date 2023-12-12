from django.contrib import admin
from .models import Exercise 
# Register your models here.

class Amin(admin.ModelAdmin):
    list_display = ("title" , "difficulty_level", "question", "answers")


admin.site.register(Exercise, Amin)