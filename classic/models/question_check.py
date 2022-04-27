from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.apps import apps

Question = apps.get_model('classic', 'Question', require_ready=False)
User = get_user_model()


class QuestionCheck(models.Model):
    '''
        お題の校閲
    '''
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name='お題',
        related_name="question_checks",
        related_query_name="question_check",
    )
    checker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='校閲者',
        related_name="question_checks",
        related_query_name="question_check",
    )
    CHECK_CHOICES = [
        (0, 'いいね！'),
        (1, 'う〜ん...'),
    ]
    choice = models.IntegerField(
        verbose_name='評価',
        choices=CHECK_CHOICES,
        default=0
    )
    timestamp = models.DateTimeField(verbose_name='校閲時刻', default=timezone.now)

    def __str__(self):
        return self.question.text

    class Meta:
        verbose_name = 'お題校閲'
        verbose_name_plural = 'お題校閲'
        ordering = ['id', ]
        constraints = [
            models.UniqueConstraint(
                fields=['question', 'checker'],
                name='unique_question_check'
            )
        ]
