# Generated by Django 4.0.4 on 2022-05-19 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scramble', '0002_match_date_asked_match_date_marked_match_is_asked_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answercomment',
            name='text',
            field=models.CharField(max_length=20, verbose_name='コメント'),
        ),
    ]
