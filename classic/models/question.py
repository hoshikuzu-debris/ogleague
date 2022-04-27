from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Question(models.Model):
    '''
    お題は
        create: お題を投稿する
        ask: お題が出題される
        mark: 制限時間まで採点される
        marked: 採点が終了され公開される
    の順に遷移する
    '''
    questioner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name='出題者',
        related_name="created_questions",
        related_query_name="created_question",
    )
    image = models.ImageField(
        "お題画像",
        upload_to='image/classic/question_image/',
        blank=True,
        null=True
    )
    text = models.CharField(verbose_name='お題', max_length=60)
    date_created = models.DateTimeField(verbose_name='作成時刻', auto_now_add=True)
    was_checked = models.BooleanField(
        '校閲済み',
        default=False,
    )
    is_safe =   models.BooleanField(
        '出題可能',
        default=False,
    )
    was_asked = models.BooleanField(
        '出題済み',
        default=False,
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'お題'
        verbose_name_plural = 'お題'
        ordering = ['-id', ]