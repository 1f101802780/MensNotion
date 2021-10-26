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
    image = forms.FileField(required=False)

    class Meta:
        model = Post
        exclude = ['user', 'favorite', 'created_at']
        labels = {
            'title': 'タイトル',
            'image': '画像',
            'text': '説明',
            'category': 'カテゴリー'
        }

class CommentForm(BaseForm):
    class Meta:
        model = Comment
        fields =('text',)

class QuestionForm(BaseForm):
    image = forms.FileField(required=False)

    class Meta:
        model = Question
        exclude = ['good_question', 'good_answer', 'created_at']
        label = {
            'title': 'タイトル',
            'text': '本文',
            'image': '画像',
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