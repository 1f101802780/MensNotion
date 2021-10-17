from django import forms
from django.core import validators
from .models import Question, Post, User


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

class UserAddForm(BaseForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password']
