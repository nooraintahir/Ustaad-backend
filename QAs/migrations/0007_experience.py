# Generated by Django 5.0 on 2024-03-27 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QAs', '0006_previous_lessonplan'),
    ]

    operations = [
        migrations.CreateModel(
            name='experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experience_level', models.IntegerField(default=0)),
                ('preferred_frequency', models.IntegerField(default=0)),
            ],
        ),
    ]