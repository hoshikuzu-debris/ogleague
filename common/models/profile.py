from django.db import models
from django.contrib.auth import get_user_model
from django.apps import apps


Level = apps.get_model('classic', 'Level', require_ready=False)
User = get_user_model()

def get_or_create_default_level():
    default_level, created = Level.objects.get_or_create(name='C')
    return default_level

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    icon = models.ImageField(
        verbose_name="アイコン",
        upload_to='image/common/user_icon/',
        default='image/common/user_icon/hiyokko.png'
    )
    bio = models.CharField(
        '自己紹介',
        blank = True,
        max_length=140,
        help_text='最大140文字です。',
    )
    classic_level = models.ForeignKey(
        Level,
        verbose_name="レベル",
        on_delete=models.PROTECT,
        default=get_or_create_default_level,
        related_name="users",
        related_query_name="user",
    )

    class Meta:
        verbose_name = "プロフィール"
        verbose_name_plural = "プロフィール"

    def __str__(self):
        return self.user.username