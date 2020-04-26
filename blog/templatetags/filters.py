from django import template

register = template.Library()


@register.filter(name='post_status')
def post_status(posts, status):
    return posts.filter(status=status).count()