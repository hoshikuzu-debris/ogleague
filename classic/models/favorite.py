from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.apps import apps

Answer = apps.get_model('classic', 'Answer', require_ready=False)
User = get_user_model()


class Favorite(models.Model):
    """
    お気に入り
    """
    answer = models.ForeignKey(
        Answer,
        verbose_name='回答',
        on_delete=models.CASCADE,
        related_name="favorites",
        related_query_name="favorite",
    )
    user = models.ForeignKey(
        User,
        verbose_name='ユーザー',
        on_delete=models.CASCADE,
        related_name="favorites",
        related_query_name="favorite",
    )
    timestamp = models.DateTimeField(verbose_name='登録時刻', default=timezone.now)

    def __str__(self):
        return self.answer.text

    class Meta:
        verbose_name = 'お気に入り'
        verbose_name_plural = 'お気に入り'
        ordering = ['-id', ]
        constraints = [
            models.UniqueConstraint(
                fields=['answer', 'user'],
                name='unique_favorite_answer_user'
            ),
        ]