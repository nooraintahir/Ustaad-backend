# Generated by Django 4.2.6 on 2023-10-19 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QAs', '0004_alter_exercise_difficulty_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='answers',
            field=models.CharField(default=0, max_length=1000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='exercise',
            name='difficulty_level',
            field=models.CharField(choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')], max_length=50),
        ),
    ]