from django.db import models
from django.contrib.auth import get_user_model
from django.apps import apps

Answer = apps.get_model('classic', 'Answer', require_ready=False)
User = get_user_model()


class AnswerReview(models.Model):
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        verbose_name='投票回答',
        related_name="answer_reviews",
        related_query_name="answer_review",
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name='投票者',
        blank=True,
        related_name="answer_reviews",
        related_query_name="answer_review",
    )
    POINT_CHOICES = [
        (0, '0点'),
        (2, '2点'),
        (3, '3点'),
        (4, '4点')
    ]
    point = models.IntegerField(
        verbose_name='点数',
        choices=POINT_CHOICES,
        blank=True,
        default=0
    )
    comment = models.CharField(
        verbose_name='コメント',
        blank=True,
        max_length=20,
    )


    class Meta:
        verbose_name = '採点詳細'
        verbose_name_plural = '採点詳細'
        ordering = ['-id', ]
        constraints = [
            models.UniqueConstraint(
                fields=['answer', 'reviewer'],
                name='unique_answer_review'
            )
        ]
