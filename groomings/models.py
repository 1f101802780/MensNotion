from django.db import models
from django.db.models.deletion import CASCADE, SET, SET_NULL
from django.db.models.fields import related
from django.utils.timezone import now
from django.core.validators import MinValueValidator

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
    title = models.CharField(max_length=30, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name="user_post"
    )
    favorite = models.ManyToManyField(User, related_name="user_favo_post")
    category = models.CharField(max_length=15, default='カテゴリーなし')

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
    title = models.CharField(max_length=30, null=True, blank=True)
    text = models.TextField(null=False, blank=False)
    give_point = models.IntegerField(blank=False, null=False, default=5, validators=[MinValueValidator(5)])
    giver = models.ForeignKey(
        'User', on_delete=CASCADE, related_name="user_give_question"
    )
    recipient = models.ForeignKey(
        'User', on_delete=SET_NULL, null=True, related_name="user_receive_question"
    )
    # userインスタンス.user_good_question.all() でその被質問者が「いい質問ですね(質問に対するいいね)」をした投稿を取得
    good_question = models.ManyToManyField(User, related_name="user_good_question")
    # Userインスタンス.user_good_answer.all() で質問者が「ありがとう！(答えに対するいいね)」をした投稿を取得
    good_answer = models.ManyToManyField(User, related_name="user_good_answer")

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
    
    class Meta:
        db_table = 'reply'
    
