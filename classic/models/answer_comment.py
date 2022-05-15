from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.apps import apps

Answer = apps.get_model('classic', 'Answer', require_ready=False)
User = get_user_model()


class AnswerComment(models.Model):
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        verbose_name='コメント回答',
        related_name="answer_comments",
        related_query_name="answer_comment",
    )
    commentator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='コメンテーター',
        related_name="answer_comments",
        related_query_name="answer_comment",
    )
    text = models.CharField(
        verbose_name='コメント',
        blank=True,
        max_length=20,
    )
    timestamp = models.DateTimeField(verbose_name='コメント時刻', default=timezone.now)


    class Meta:
        verbose_name = 'コメント'
        verbose_name_plural = 'コメント'
        ordering = ['-id', ]