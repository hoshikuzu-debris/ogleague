from django.db import models
from django.db.models import Q
from django.utils import timezone
import datetime

def after_a_week():
    return timezone.now() + datetime.timedelta(weeks=1)

def after_two_weeks():
    return timezone.now() + datetime.timedelta(weeks=2)


class Contest(models.Model):
    date_asked = models.DateTimeField(verbose_name='出題時刻', default=timezone.now)
    post_deadline = models.DateTimeField(verbose_name='回答締切時刻', default=after_a_week)
    date_marked= models.DateTimeField(verbose_name='採点終了時刻', default=after_two_weeks)
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
        return f"{self.id}"

    class Meta:
        verbose_name = 'コンテスト'
        verbose_name_plural = 'コンテスト'
        ordering = ['-id', ]
        constraints = [
            models.UniqueConstraint(
                fields=['is_held'],
                condition=Q(is_held=True),
                name='unique_is_held'
            ),
        ]
