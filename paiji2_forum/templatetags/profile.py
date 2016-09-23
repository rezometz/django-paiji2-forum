from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag
def profile_url(user):
    try:
        return reverse('forum:profile', args=[user.pk])
    except:
        return ''


@register.inclusion_tag('forum/mail_link.html')
def mail_link(user, text, subject):
    return {
        'user': user,
        'text': text,
        'subject': subject,
    }


@register.inclusion_tag('forum/profile_link.html')
def profile_link(user):
    return {
        'user': user,
    }
