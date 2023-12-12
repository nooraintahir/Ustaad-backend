from django.db import models


# Create your models here.
class Exercise(models.Model):
    DIFFICULTY_CHOICES = (
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    )

    title = models.CharField(max_length=50)
    difficulty_level = models.CharField(max_length=50, choices=DIFFICULTY_CHOICES)
    question = models.CharField(max_length=500)
    answers = models.CharField(max_length=1000)

    def __str__(self):
        return self.title 