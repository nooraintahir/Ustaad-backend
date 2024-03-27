from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


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
    user_username = models.CharField(max_length=150, default="none")  # Assuming maximum username length is 150 characters
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    score = models.BooleanField(default=False)  # True for cleared, False for not cleared
    times_attempted = models.IntegerField(default=0)
    date_attempted = models.DateTimeField(default=timezone.now)
    class Meta:
        unique_together = ['user_username', 'question']

    def __str__(self):
        return f"{self.user_username} - {self.question.question_text}"

class Add_Question(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=100)
    question_difficulty = models.CharField(max_length=10)
    question_text = models.TextField()
    question_topic = models.CharField(max_length=10)

    def __str__(self):
        return self.question_text
    
class LessonPlan(models.Model):
    topic = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=10)
    questions_to_attempt = models.IntegerField(default=0)
    questions_attempted = models.IntegerField(default=0)
    username = models.CharField(max_length=150, default="none")  # Assuming maximum username length is 150 characters
    date_created = models.DateTimeField(default=timezone.now)
    completed = models.IntegerField(default=0) #`0` for `False` and `1` for `True`

    def __str__(self):
        return self.topic
    
class Previous_LessonPlan(models.Model):
    timestamp = models.DateTimeField()
    topic = models.CharField(max_length=100)
    questions_present = models.TextField()
    username = models.CharField(max_length=150, default="none")

    def __str__(self):
        return f"Question - Topic: {self.topic}, Timestamp: {self.timestamp}"
    
class experience(models.Model):
    experience_level = models.IntegerField(default=0)
    preferred_frequency =models.IntegerField(default=0)
