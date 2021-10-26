from django import forms
from .models import Comment, Question, Post, Reply, User
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
    class Meta:
        model = Post
        exclude = ['favorite', 'created_at']
        labels = {
            'title': 'タイトル',
            'image': '画像',
            'text': '説明',
            'category': 'カテゴリー',
            'user': 'ユーザー(ログイン処理作ったら消す)'
        }

class CommentForm(BaseForm):
    class Meta:
        model = Comment
        fields =('user', 'text', 'post')

class QuestionForm(BaseForm):
    class Meta:
        model = Question
        exclude = ['good_question', 'good_answer']
        label = {
            'title': 'タイトル',
            'text': '本文',
            'give_point': '付与するポイント',
            'giver': '自分(ログイン処理作ったら消す)',
            'recipient': '質問する相手'
        }

class ReplyForm(BaseForm):
    class Meta:
        model = Reply
        exclude = ['created_at']

    def clean(self):
        cleaned_data = super().clean()
        question = cleaned_data.get('question')
        giver = cleaned_data.get('giver')
        recipient = cleaned_data.get('recipient')
        if not question.giver in [giver, recipient]:
            raise ValidationError('匿名質問の質問者か回答者しかリプできません')
        if not question.recipient in [giver, recipient]:
            raise ValidationError('匿名質問の質問者か回答者にしかリプできません')
        if question.giver == question.recipient:
            raise ValidationError('質問者と回答者が同じです')

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