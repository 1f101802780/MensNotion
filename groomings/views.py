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
