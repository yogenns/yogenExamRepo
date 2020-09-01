# Generated by Django 3.0.3 on 2020-09-01 05:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam_app', '0003_exam'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='passing_percentage',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)]),
        ),
    ]