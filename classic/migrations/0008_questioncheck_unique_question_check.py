# Generated by Django 4.0.4 on 2022-04-22 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classic', '0007_answerreview_unique_answer_review'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='questioncheck',
            constraint=models.UniqueConstraint(fields=('question', 'checker'), name='unique_question_check'),
        ),
    ]
