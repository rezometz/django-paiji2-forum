from django import template
from ..models import Message


register = template.Library()


@register.inclusion_tag(
    'forum/forum_block.html',
    takes_context=True,
)
def get_forum(context, nb=15):
    return {
        'messages': Message.objects.exclude(
                readers__pk=context['request'].user.pk
            ).order_by(
                '-pub_date'
            ).all()[:nb],
        'user': context['request'].user,
    }
