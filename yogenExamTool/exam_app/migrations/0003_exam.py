# Generated by Django 3.0.3 on 2020-08-31 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam_app', '0002_question'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('question_count', models.PositiveSmallIntegerField()),
                ('time', models.TimeField()),
                ('passing_percentage', models.DecimalField(decimal_places=2, max_digits=4)),
                ('questions', models.ManyToManyField(to='exam_app.Question')),
            ],
        ),
    ]
