from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Subscriber, Post


@shared_task
def send_email_task(pk):
    post = Post.objects.get(pk=pk)
    title = post.title
    category = post.category
    subscribers_emails = []
    subscribers = Subscriber.objects.filter(category=category)
    subscribers_emails += [subs.user.email for subs in subscribers]
    html_content = render_to_string(
        'daily_post.html',
        {
            'text': f'{post.title}',
            'link': f'{settings.SITE_URL}/news/{pk}'

        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_emails,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()