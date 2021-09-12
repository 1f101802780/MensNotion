from django.shortcuts import render
from groomings.models import User, Post

# Create your views here.
def top(request):
    """トップ画面"""
    posts = Post.objects.order_by('-created_at')
    return render(request, 'groomings/top.html', context={"posts": posts})

def login(request):
    """ログイン画面"""
    return render(request, 'groomings/login.html')

def signup(request):
    """サインアップ画面"""
    return render(request, 'groomings/signup.html')

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
