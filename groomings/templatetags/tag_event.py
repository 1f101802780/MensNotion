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

@register.filter(name="count_follow")
def count_follow(user):
    return user.follow.all().count()

@register.filter(name="count_follower")
def count_follwer(user):
    return user.follower.all().count()

@register.filter(name="count_my_post")
def count_my_post(user):
    return user.user_post.all().count()

@register.filter(name="count_my_favo")
def count_my_favo(user):
    return user.user_favo_post.all().count()

@register.filter(name="count_unvisit")
def count_unvisit(notifys):
    return notifys.filter(is_visited=False).count()

@register.filter(name="count_nonactive")
def count_nonactive(user):
    return user.user_receive_question.filter(is_active=False).count()