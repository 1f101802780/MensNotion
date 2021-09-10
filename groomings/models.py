from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields import related
from django.utils.timezone import now
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
    """日付と時間モデル(抽象モデル)"""
    created_at = models.DateTimeField(default=now)

    class Meta:
        abstract = True


class Post(Date):
    """投稿モデル"""
    text = models.TextField(null=True, blank=True)
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name="user_post"
    )
    favorite = models.ManyToManyField(User, related_name="user_favo_post")

    class Meta:
        db_table = 'post'


class Comment(Date):
    """投稿に対するコメントモデル"""
    text = models.TextField(null=False, blank=False)
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name="user_comment"
    )
    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE
    )
    favorite = models.ManyToManyField(User, related_name="user_favo_comme")
    
    class Meta:
        db_table = 'comment'


class Question(Date):
    """匿名質問モデル"""
    text = models.TextField(null=False, blank=False)
    giver = models.ForeignKey(
        'User', on_delete=CASCADE, related_name="user_give_question"
    )
    recipient = models.ForeignKey(
        'User', on_delete=SET_NULL, null=True, related_name="user_receive_question"
    )

    class Meta:
        db_table = 'question'


class Reply(Date):
    """質問に対する返答モデル"""
    text = models.TextField(null=False, blank=False)
    question = models.ForeignKey(
        'Question', on_delete=CASCADE
    )
    giver = models.ForeignKey(
        'User', on_delete=SET_NULL, null=True, related_name="user_give_reply"
    )
    recipient = models.ForeignKey(
        'User', on_delete=SET_NULL, null=True, related_name="user_receive_reply"
    )
    
