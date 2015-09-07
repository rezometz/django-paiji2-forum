from django import template
from ..models import Message
from django.db.models import Count


register = template.Library()


@register.inclusion_tag(
    'forum/forum_block.html',
    takes_context=True,
)
def get_forum(context, nb=15):
    return {
        'messages': Message.objects.defer(
                'text',
            ).exclude(
                readers__pk=context['request'].user.pk
            ).order_by(
                '-pub_date'
            ).select_related(
                'author',
                'icon',
            ).annotate(
                readings=Count('readers'),
            )[:nb]
    }
