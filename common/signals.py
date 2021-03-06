from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import Profile


User = get_user_model()

@receiver(post_save, sender=User)
def create_profile(sender, instance=None, created=False, **kwargs):
    """新しくユーザーを作成したときにprofileも作成する"""
    if created:
        Profile.objects.create(user=instance)