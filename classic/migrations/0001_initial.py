# Generated by Django 4.0.4 on 2022-04-20 15:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='回答')),
                ('rank', models.IntegerField(default=0, verbose_name='順位')),
                ('score', models.IntegerField(default=0, verbose_name='得点')),
                ('date_answered', models.DateTimeField(default=django.utils.timezone.now, verbose_name='回答時刻')),
            ],
            options={
                'verbose_name': '回答',
                'verbose_name_plural': '回答',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='AnswerReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point', models.IntegerField(blank=True, choices=[(0, '0点'), (2, '2点'), (3, '3点'), (4, '4点')], default=0, verbose_name='点数')),
                ('comment', models.CharField(blank=True, max_length=20, verbose_name='コメント')),
            ],
            options={
                'verbose_name': '採点詳細',
                'verbose_name_plural': '採点詳細',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_asked', models.DateTimeField(default=django.utils.timezone.now, verbose_name='出題時刻')),
                ('date_marked', models.DateTimeField(blank=True, null=True, verbose_name='採点終了時刻')),
                ('is_asked', models.BooleanField(default=False, verbose_name='出題中')),
                ('is_marked', models.BooleanField(default=False, verbose_name='採点中')),
                ('was_marked', models.BooleanField(default=False, verbose_name='採点済み')),
            ],
            options={
                'verbose_name': 'コンテスト',
                'verbose_name_plural': 'コンテスト',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='登録時刻')),
            ],
            options={
                'verbose_name': 'お気に入り',
                'verbose_name_plural': 'お気に入り',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, unique=True, verbose_name='レベル')),
            ],
            options={
                'verbose_name': 'レベル',
                'verbose_name_plural': 'レベル',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'マッチ',
                'verbose_name_plural': 'マッチ',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='image/classic/question_image/', verbose_name='お題画像')),
                ('text', models.CharField(max_length=60, verbose_name='お題')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='作成時刻')),
                ('was_checked', models.BooleanField(default=False, verbose_name='校閲済み')),
                ('is_safe', models.BooleanField(default=False, verbose_name='出題可能')),
                ('was_asked', models.BooleanField(default=False, verbose_name='出題済み')),
            ],
            options={
                'verbose_name': 'お題',
                'verbose_name_plural': 'お題',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='QuestionCheck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.IntegerField(choices=[(0, 'いいね！'), (1, 'う〜ん...')], default=0, verbose_name='評価')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='校閲時刻')),
            ],
            options={
                'verbose_name': 'お題校閲',
                'verbose_name_plural': 'お題校閲',
                'ordering': ['id'],
            },
        ),
    ]