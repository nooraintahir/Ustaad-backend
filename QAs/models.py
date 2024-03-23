from django.db import models
from django.contrib.auth.models import AbstractUser

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

class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    # Add related_name for groups and user_permissions
    groups = models.ManyToManyField('auth.Group', related_name='custom_user_set')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_set')

    def __str__(self):
        return self.username

class Question(models.Model):
    question_text = models.TextField()
    topic = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=10)

    def __str__(self):
        return self.question_text

class UserQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    score = models.BooleanField(default=False)  # True for cleared, False for not cleared

    class Meta:
        unique_together = ['user', 'question']  # Ensures each user has only one instance of each question

    def __str__(self):
        return f"{self.user.username} - {self.question.question_text}"

class Add_Question(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=100)
    question_difficulty = models.CharField(max_length=10)
    question_text = models.TextField()
    question_topic = models.CharField(max_length=10)

    def __str__(self):
        return self.question_text