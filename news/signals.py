from django.db.models.signals import post_save
from django.dispatch import receiver

from NewsPaper.news.models import Post
from .tasks import send_email_task

@receiver(post_save, sender=Post)
def notify_about_new_post(sender, instance, created, **kwargs):
    if created:
        send_email_task.delay(instance.pk)