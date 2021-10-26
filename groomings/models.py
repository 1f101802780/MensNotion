from django.db import models
from django.db.models.deletion import CASCADE, SET, SET_NULL
from django.db.models.fields import related
from django.utils.timezone import now
from django.core.validators import MinValueValidator
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Enter Email')
        user = self.model(    # 下に書いたユーザークラスを呼び出す
            username = username,
            email = email,
            # それ以外のフィールドはデフォルトで設定される
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.model(
            username = username,
            email = email,
        )
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

        
class User(AbstractBaseUser, PermissionsMixin):
    """ユーザーモデル"""
    # passwordはすでにAbstractBaseUserにあるから書かない
    # is_superuser(スーパーユーザーかどうか)もPermissionsMixinに書いてあるから書かない
    username = models.CharField(max_length=150)
    email = models.EmailField(max_length=255, unique=True)
    point = models.IntegerField(default=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # 管理画面にログインできるかどうか

    USERNAME_FIELD = 'email' # このテーブルのレコードを一意に識別
    REQUIRED_FIELDS = ['username'] # スーパーユーザー作成時に入力する(emailとパスワードは必須だからそれ以外で)

    objects = UserManager()

    def __str__(self):
        return self.email


class Date(models.Model):
    """日付と時間モデル(抽象モデル)"""
    created_at = models.DateTimeField(default=now)

    class Meta:
        abstract = True


class Post(Date):
    """投稿モデル"""
    title = models.CharField(max_length=30, null=True, blank=True)
    image = models.FileField(upload_to='post_image/', null=True)
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
        'Post', on_delete=models.CASCADE, related_name="post_comment"
    )
    favorite = models.ManyToManyField(User, related_name="user_favo_comme")
    
    class Meta:
        db_table = 'comment'


class Question(Date):
    """匿名質問モデル"""
    title = models.CharField(max_length=30, null=True, blank=True)
    text = models.TextField(null=False, blank=False)
    image = models.FileField(upload_to='question_image/', null=True)
    give_point = models.IntegerField(blank=False, null=False, default=5, validators=[MinValueValidator(5)])
    
    # 質問する人
    giver = models.ForeignKey(
        'User', on_delete=CASCADE, related_name="user_give_question"
    )

    # 質問される人
    recipient = models.ForeignKey(
        'User', on_delete=SET_NULL, null=True, related_name="user_receive_question"
    )
    # Userインスタンス.user_good_question.all() でその被質問者が「いい質問ですね(質問に対するいいね)」をした投稿を取得
    good_question = models.ManyToManyField(User, related_name="user_good_question")
    # Userインスタンス.user_good_answer.all() で質問者が「ありがとう！(答えに対するいいね)」をした投稿を取得
    good_answer = models.ManyToManyField(User, related_name="user_good_answer")

    class Meta:
        db_table = 'question'


class Reply(Date):
    """質問に対する返答モデル"""
    text = models.TextField(null=False, blank=False)
    image = models.FileField(upload_to='reply_image/', null=True)
    question = models.ForeignKey(
        'Question', on_delete=CASCADE, related_name="question_reply"
    )

    # リプライした人
    giver = models.ForeignKey(
        'User', on_delete=SET_NULL, null=True, related_name="user_give_reply"
    )

    # リプライ受け取った人
    recipient = models.ForeignKey(
        'User', on_delete=SET_NULL, null=True, related_name="user_receive_reply"
    )
    
    class Meta:
        db_table = 'reply'
    
