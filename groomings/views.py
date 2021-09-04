from django.shortcuts import render

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
    data = {"user": user_id} # 実際のユーザーデータはモデルを作ってから代入します。
    return render(request, 'groomings/user.html', data)
