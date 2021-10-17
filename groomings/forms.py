from django import forms
from django.core import validators
from .models import Question, Post, User
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UsernameField
from django.core.exceptions import ValidationError
from django.forms.widgets import PasswordInput


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
        user.set_password(self.cleaned_data.get("password"))
        user.save()
        return user

# ユーザー情報変更用のフォーム
class UserChangeForm(BaseForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_staff', 'is_active', 'is_superuser')

    def clean_password(self):
        # すでに登録されているパスワードを返す(パスワードを変更できないようにする)
        return self.initial['password']