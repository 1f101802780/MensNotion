from django.db.models.fields import EmailField
from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from groomings.models import User, Post, Comment, Question, Reply

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

def edit_user(request, user_id):
    """ユーザー情報編集ページ"""
    user = User.objects.get(pk=user_id)
    return render(request, 'groomings/edit_user.html', context={"user": user})

def create_post(request): # user_id)

    form = forms.PostForm()
    if request.method == 'POST':
        form = forms.PostForm(request.POST, request.FILES)
        if form.is_valid(): # バリデーションがOKなら保存
            form.save()
            return redirect('groomings:top')
    # if form.is_valid():
    #     post = form.save(commit=False)
    #     post.image = request.FILES['image']  
    #     post.user = request.user
    #     post.save()
    #     messages.info(request, f'記事を作成しました。 タイトル:{post.title} pk:{post.pk}')
    #     return redirect('post:list_index')
    # else:
    #     messages.error(request, '失敗しました', extra_tags='danger')
    #     return redirect('post:list_index')

    # else:
    #     form = PostForm(instance=post)

    return render(request, 'groomings/create_post.html', context={"form": form}) # , 'id': user_id})

def ranking(request):
    """ランキング用のページ"""
    return render(request, 'groomings/ranking.html')

# 投稿詳細ページ
def post_detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    comme_form = forms.CommentForm()
    if request.method == 'POST':
        comme_form = forms.CommentForm(request.POST)
        if comme_form.is_valid():
            comme_form.save()
            return redirect('groomings:top')
    return render(request, 'groomings/post_detail.html', context={"post": post, "form": comme_form})

def question_detail(request, question_id):
    question = Question.objects.get(pk=question_id)
    rep_form = forms.ReplyForm()
    if request.method == 'POST':
        rep_form = forms.ReplyForm(request.POST)
        if rep_form.is_valid():
            rep_form.save()
            return redirect('groomings:top')
    return render(request, 'groomings/question_detail.html', context={"question": question, "form": rep_form})


