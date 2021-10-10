from django.shortcuts import render, redirect
from . import forms
from groomings.models import User, Post, Comment, Question, Reply

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

def list_create(request): # user_id)

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

    return render(request, 'groomings/list_create.html', context={"form": form}) # , 'id': user_id})
