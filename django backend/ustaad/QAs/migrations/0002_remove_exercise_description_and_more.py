# Generated by Django 4.2.6 on 2023-10-18 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QAs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exercise',
            name='description',
        ),
        migrations.AlterField(
            model_name='exercise',
            name='difficulty_level',
            field=models.CharField(choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], max_length=50),
        ),
    ]