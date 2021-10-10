from django import forms
from django.core import validators
from .models import User, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['favorite', 'created_at']
        labels = {
            'title':'タイトル',
            'text':'説明',
            'category':'カテゴリー',
            'user': 'ユーザー(ログイン処理作ったら消す)'
        }
    
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label