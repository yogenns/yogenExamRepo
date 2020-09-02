# Generated by Django 3.0.3 on 2020-09-02 07:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam_app', '0005_examattempt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examattempt',
            name='result_attempted_question_count',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='examattempt',
            name='result_correct_answer_count',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='examattempt',
            name='result_percentage',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)]),
        ),
    ]
