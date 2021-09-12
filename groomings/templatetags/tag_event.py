from django import template


register = template.Library()

@register.filter(name="count_favo")
def count_favo(post):
    return post.favorite.all().count()