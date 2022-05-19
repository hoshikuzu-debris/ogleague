from django.db import models
from django.apps import apps
from django.db import models
from django.db.models import Q
from django.utils import timezone
import datetime

Question = apps.get_model('scramble', 'Question', require_ready=False)
Level = apps.get_model('scramble', 'Level', require_ready=False)


def after_ten_minutes():
    return timezone.now() + datetime.timedelta(minutes=10)


class Match(models.Model):
    question = models.OneToOneField(
        Question,
        verbose_name='お題',
        on_delete=models.CASCADE,
    )
    level = models.ForeignKey(
        Level,
        verbose_name='レベル',
        on_delete=models.CASCADE,
        related_name="matches",
        related_query_name="match",
    )
    date_asked = models.DateTimeField(verbose_name='出題時刻', default=timezone.now)
    post_deadline = models.DateTimeField(verbose_name='回答締切時刻', default=after_ten_minutes)
    date_marked= models.DateTimeField(verbose_name='採点終了時刻', default=after_ten_minutes)
    is_held = models.BooleanField(
        '開催中',
        default=False,
    )
    is_asked = models.BooleanField(
        '出題中',
        default=False,
    )
    is_marked = models.BooleanField(
        '採点中',
        default=False,
    )
    was_marked = models.BooleanField(
        '採点済み',
        default=False,
    )

    def __str__(self):
        return self.question.text

    class Meta:
        verbose_name = 'マッチ'
        verbose_name_plural = 'マッチ'
        ordering = ['-id', ]
        constraints = [
            models.UniqueConstraint(
                fields=['is_held'],
                condition=Q(is_held=True),
                name='unique_scr_is_held'
            ),
        ]
