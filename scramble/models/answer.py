from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.apps import apps

Question = apps.get_model('scramble', 'Question', require_ready=False)
Match = apps.get_model('scramble', 'Match', require_ready=False)
User = get_user_model()


class Answer(models.Model):
    '''
    ボケは
        create: お題を投稿する
        ask: お題が出題される
        mark: 制限時間まで採点される
        marked: 採点が終了される
    の順に遷移する
    '''
    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        verbose_name='マッチ',
        related_name="answers",
        related_query_name="answer",
    )
    panellist = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name='回答者',
        related_name="scr_answers",
        related_query_name="scr_answer",
    )
    text = models.TextField(verbose_name='回答')
    rank = models.IntegerField(verbose_name='順位', default=0)
    score = models.IntegerField(verbose_name='得点', default=0)
    date_answered = models.DateTimeField(verbose_name='回答時刻', default=timezone.now)

    def __str__(self):
        return self.text

    # def get_favorite_users(self):
    #     user_list = [favorite.user for favorite in self.favorites.all()]
    #     return user_list

    #def get_score(self):
        #return self.answer_reviews.aggregate(models.Sum('point'))['point__sum']

    class Meta:
        verbose_name = '回答'
        verbose_name_plural = '回答'
        ordering = ['-id', ]

