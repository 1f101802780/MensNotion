# Generated by Django 3.2.5 on 2021-09-11 08:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groomings', '0003_create_question_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='give_point',
            field=models.IntegerField(default=5, validators=[django.core.validators.MinValueValidator(5)]),
        ),
    ]