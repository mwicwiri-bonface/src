# Generated by Django 3.2.4 on 2021-07-20 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainee', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainingapplication',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
