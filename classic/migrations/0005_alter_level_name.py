# Generated by Django 4.0.4 on 2022-04-21 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classic', '0004_contest_is_held_contest_unique_is_held'),
    ]

    operations = [
        migrations.AlterField(
            model_name='level',
            name='name',
            field=models.SlugField(unique=True, verbose_name='レベル'),
        ),
    ]
