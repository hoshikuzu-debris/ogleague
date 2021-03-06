# Generated by Django 4.0.4 on 2022-04-21 14:57

import classic.models.contest
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classic', '0005_alter_level_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='post_deadline',
            field=models.DateTimeField(default=classic.models.contest.after_a_week, verbose_name='回答締切時刻'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='date_marked',
            field=models.DateTimeField(default=classic.models.contest.after_two_weeks, verbose_name='採点終了時刻'),
        ),
    ]
