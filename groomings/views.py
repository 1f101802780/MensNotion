from django.shortcuts import render
from groomings.models import User

# Create your views here.
def top(request):
    """トップ画面"""
    return render(request, 'groomings/top.html')

def login(request):
    """ログイン画面"""
    return render(request, 'groomings/login.html')

def signup(request):
    """サインアップ画面"""
    return render(request, 'groomings/signup.html')

def user(request, user_id):
    """ユーザーページ"""
    user = User.objects.get(pk=user_id)
    return render(request, 'groomings/user.html', context={"user": user})

def edit_user(request, user_id):
    """ユーザー情報編集ページ"""
    user = User.objects.get(pk=user_id)
    return render(request, 'groomings/edit_user.html', context={"user": user})
