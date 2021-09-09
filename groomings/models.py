from django.db import models
from django.utils import timezone
import pytz

# Create your models here.
class User(models.Model):
    """ユーザーモデル"""
    name = models.CharField(max_length=10)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    point = models.IntegerField(default=0)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.name


class Date(models.Model):
    created_at = models.DateTimeField(default=timezone.datetime.now(pytz.timezone('Asia/Tokyo')))

    class Meta:
        abstract = True


class Post(Date):
    """投稿モデル"""
    text = models.TextField(null=True, blank=True)
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name = "user_post"
    )
    favorite = models.ManyToManyField(User, related_name = "user_favo_post")

    class Meta:
        db_table = 'post'


class Comment(Date):
    """投稿に対するコメントモデル"""
    text = models.TextField(null=False, blank=False)
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name = "user_comment"
    )
    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE
    )
    favorite = models.ManyToManyField(User, related_name = "user_favo_comme")
    
    class Meta:
        db_table = 'comment'