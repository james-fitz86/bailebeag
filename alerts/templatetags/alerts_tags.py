from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def unread_alerts_count(context):
    user = context.get("user")
    if not user or not user.is_authenticated:
        return 0
    return user.notifications.filter(is_read=False).count()