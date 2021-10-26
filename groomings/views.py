from django.db.models.fields import EmailField
from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from groomings.models import User, Post, Comment, Question, Reply
from django.contrib import messages

# Create your views here.
def top(request):
    """トップ画面"""
    posts = Post.objects.order_by('-created_at')
    return render(request, 'groomings/top.html', context={"posts": posts})

def user_login(request):
    """ログイン画面"""
    login_form = forms.LoginForm(request.POST or None)
    if login_form.is_valid():
        email = login_form.cleaned_data.get('email')
        password = login_form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            if user.is_active:
                login(request, user) # ログイン
                messages.success(request, 'ログインしました')
                return redirect('groomings:top')
    return render(request, 'groomings/login.html', context={
        'login_form': login_form
    })

def user_signup(request):
    """サインアップ画面"""
    message = ''  # 初期表示ではカラ
    form = forms.UserAddForm()
    if (request.method == 'POST'):
        form = forms.UserAddForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            try:
                validate_password(form.cleaned_data.get('password'), user)
            except ValidationError as e:
                form.add_error('password', e) # formのパスワードの部分にエラー内容を追加
                return render(request, 'groomings/signup.html', context={
                    'form': form
                })
            user.set_password(user.password) # passwordの暗号化
            user.save()
            return redirect(to='/login') # パスワードのエラーもなければログイン画面にリダイレクト
        else:
            message = '再入力して下さい'

    modelform_dict = {
        'form': form,
        'message': message, #エラーメッセージ
    }
    return render(request, 'groomings/signup.html', modelform_dict)


def user(request, user_id):
    """ユーザーページ"""
    user = User.objects.get(pk=user_id)
    posts = user.user_post.all()
    posts_count = user.user_post.all().count()
    favo_count = user.user_favo_post.all().count()
    return render(request, 'groomings/user.html', context={"user": user, "posts": posts, "posts_count": posts_count, "favo_count": favo_count})

def user_favo(request, user_id):
    user = User.objects.get(pk=user_id)
    favo_posts = user.user_favo_post.all()
    posts_count = user.user_post.all().count()
    favo_count = favo_posts.count()
    return render(request, 'groomings/user_favo.html', context={"user": user, 'favo_posts': favo_posts, "posts_count": posts_count, "favo_count": favo_count})

@login_required
def edit_user(request):
    """ユーザー情報編集ページ"""
    edit_user_form = forms.UserEditForm(request.POST or None, instance=request.user)
    if edit_user_form.is_valid():
        edit_user_form.save()
        messages.success(request, 'ユーザー情報を更新しました')
    return render(request, 'groomings/edit_user.html', context={"edit_user_form": edit_user_form})

@login_required
def change_password(request):
    password_change_form = forms.PasswordChangeForm(request.POST or None, instance=request.user)
    if password_change_form.is_valid():
        try:
            password_change_form.save()
            messages.success(request, 'パスワードを変更しました')
            update_session_auth_hash(request, request.user)
        except ValidationError as e:
            password_change_form.add_error('password', e)
    return render(request, 'groomings/change_password.html', context={
        'password_change_form': password_change_form
        })



@login_required
def create_post(request): # user_id)
    form = forms.PostForm(request.POST or None, request.FILES or None)
    if form.is_valid(): # バリデーションがOKなら保存
        form.instance.user = request.user
        toukou = form.save()
        messages.info(request, f'投稿しました。ユーザー:{toukou.user} タイトル:{toukou.title} pk:{toukou.pk}')
        return redirect('groomings:top')
    return render(request, 'groomings/create_post.html', context={"form": form}) # , 'id': user_id})

def ranking(request):
    """ランキング用のページ"""
    return render(request, 'groomings/ranking.html')

# 投稿詳細ページ
@login_required
def post_detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    comme_form = forms.CommentForm(request.POST or None)
    if comme_form.is_valid():
        if request.user.point > 70: # ログインユーザーのポイントが70より大きくなければコメントできない
            comme_form.instance.user = request.user
            comme_form.instance.post = post
            comme_form.save()
            messages.success(request, 'コメントしました')
            return redirect('groomings:top')
        else:
            messages.warning(request, '所持ポイントが足りません')
    comments = post.post_comment.all()
    return render(request, 'groomings/post_detail.html', context={"post": post, "form": comme_form, "comments": comments})

@login_required
def question_detail(request, question_id):
    question = Question.objects.get(pk=question_id)
    question_users = [question.giver, question.recipient]
    if not request.user in question_users:
        return redirect('groomings:top')
    rep_form = forms.ReplyForm(request.POST or None)
    if rep_form.is_valid():
        rep_form.instance.question = question
        rep_form.instance.giver = request.user
        if question.giver == request.user:
            rep_form.instance.recipient = question.recipient
        else:
            rep_form.instance.recipient = question.giver
        rep_form.save()
        return redirect('groomings:question_detail', question_id=question.id)
    replys = question.question_reply.all()
    return render(request, 'groomings/question_detail.html', context={"question": question, "form": rep_form, "replys": replys})


