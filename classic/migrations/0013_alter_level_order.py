# Generated by Django 4.0.4 on 2022-04-29 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classic', '0012_level_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='level',
            name='order',
            field=models.IntegerField(unique=True, verbose_name='オーダー'),
        ),
    ]
