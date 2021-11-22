from django import forms
from .models import Comment, Question, Post, Reply, User, Tag
from django.core.exceptions import ValidationError
from django.forms.widgets import PasswordInput
from django.contrib.auth.password_validation import validate_password


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class PostForm(BaseForm):
    image1 = forms.FileField(required=False)
    image2 = forms.FileField(required=False)
    image3 = forms.FileField(required=False)
    category = forms.ChoiceField(
        choices = (
            ('none_category', 'カテゴリーなし'),
            ('skincare', 'スキンケア'),
            ('make', 'メイク'),
            ('hair', 'ヘアー'),
            ('fashion', '服装'),
            ('others', 'その他')
        ),
    )

    class Meta:
        model = Post
        exclude = ['user', 'favorite', 'created_at']
        labels = {
            'title': 'タイトル',
            'image1': '画像1',
            'image2': '画像2',
            'image3': '画像3',
            'text': '説明',
            'category': 'カテゴリー'
        }

class CommentForm(BaseForm):
    class Meta:
        model = Comment
        fields =('text',)

class QuestionForm(BaseForm):
    image1 = forms.FileField(required=False)
    image2 = forms.FileField(required=False)
    image3 = forms.FileField(required=False)

    class Meta:
        model = Question
        exclude = ['good_question', 'good_answer', 'created_at']
        label = {
            'title': 'タイトル',
            'text': '本文',
            'image1': '画像1',
            'image2': '画像2',
            'image3': '画像3',
            'give_point': '付与するポイント',
            'giver': '自分(ログイン処理作ったら消す)',
            'recipient': '質問する相手'
        }

class ReplyForm(BaseForm):
    image = forms.FileField(required=False)
    
    class Meta:
        model = Reply
        fields = ('text', 'image')

# ユーザー追加用のフォーム
class UserAddForm(BaseForm):
    password = forms.CharField(label='password', widget=PasswordInput)
    confirm_password = forms.CharField(label='Password再入力', widget=PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('パスワードが一致しません')

    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)
        user.set_password(user.password)
        user.save()
        return user


class UserEditForm(BaseForm):
    username = forms.CharField(label='ユーザー名')
    email = forms.EmailField(label='メールアドレス')

    class Meta:
        model = User
        fields = ('username', 'email')

class PasswordChangeForm(BaseForm):
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='パスワード再入力', widget=forms.PasswordInput)

    class Meta():
        model = User
        fields = ('password',)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('パスワードが異なります')

    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField(label='メールアドレス', max_length=255)
    password = forms.CharField(label='パスワード', widget=PasswordInput)

class TagForm(BaseForm):
    class Meta:
        model = Tag
        fields = ('name',)
