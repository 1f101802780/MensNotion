from django import template


register = template.Library()

@register.filter(name="count_favo")
def count_favo(post):
    return post.favorite.all().count()

@register.filter(name="count_commefavo")
def count_commefavo(comment):
    return comment.favorite.all().count()

@register.filter(name="count_commebad")
def count_commebad(comment):
    return comment.bad.all().count()