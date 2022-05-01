from tokenize import Triple
from django.db import models
from django.apps import apps

Contest = apps.get_model('classic', 'Contest', require_ready=False)


class Level(models.Model):
    name = models.SlugField(
        "レベル",
        unique=True
    )
    color = models.CharField(
        "カラー",
        max_length=100,
        blank=True
    )
    order = models.IntegerField(
        'オーダー',
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'レベル'
        verbose_name_plural = 'レベル'
        ordering = ['order', ]
