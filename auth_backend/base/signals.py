# base/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Calendar, DiaryBook

@receiver(post_save, sender=CustomUser)
def create_default_calendar(sender, instance, created, **kwargs):
    if created:
        Calendar.objects.get_or_create(owner=instance, name=f"{instance.username}'s calendar")
        DiaryBook.objects.get_or_create(name=f"{instance.username}'s' diary", owner=instance, is_public=False)
