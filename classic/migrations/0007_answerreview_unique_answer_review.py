# Generated by Django 4.0.4 on 2022-04-22 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classic', '0006_contest_post_deadline_alter_contest_date_marked'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='answerreview',
            constraint=models.UniqueConstraint(fields=('answer', 'reviewer'), name='unique_answer_review'),
        ),
    ]