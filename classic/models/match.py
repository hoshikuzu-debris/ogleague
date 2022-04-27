from django.db import models
from django.apps import apps

Question = apps.get_model('classic', 'Question', require_ready=False)
Contest = apps.get_model('classic', 'Contest', require_ready=False)
Level = apps.get_model('classic', 'Level', require_ready=False)


class Match(models.Model):
    question = models.OneToOneField(
        Question,
        verbose_name='お題',
        on_delete=models.CASCADE,
    )
    contest = models.ForeignKey(
        Contest,
        verbose_name='コンテスト',
        on_delete=models.CASCADE,
        related_name="matches",
        related_query_name="match",
    )
    level = models.ForeignKey(
        Level,
        verbose_name='レベル',
        on_delete=models.CASCADE,
        related_name="matches",
        related_query_name="match",
    )

    def __str__(self):
        return self.question.text

    class Meta:
        verbose_name = 'マッチ'
        verbose_name_plural = 'マッチ'
        ordering = ['-id', ]
        constraints = [
            models.UniqueConstraint(
                fields=['contest', 'level'],
                name='unique_contest_level'
            )
        ]
