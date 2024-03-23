from rest_framework import serializers
from .models import Exercise, User

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ('title'
                   , 'difficulty_level' , 'question' ,
                   'answers')


