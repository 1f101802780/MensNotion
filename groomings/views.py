from django.db.models.fields import EmailField
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from groomings.models import User, Post, Comment, Question, Reply
from django.contrib import messages
from django.db.models import Count
from django.db.models import Q


def top(request):
    """トップ画面"""
    if request.user.is_authenticated:
        users = request.user.follow.all()
        posts = Post.objects.filter(Q(user__in=users) | Q(user=request.user)).order_by('-created_at')
    else:
        posts = Post.objects.order_by('-created_at')

    q_word = request.GET.get('query')
    if q_word:
        if request.GET.get('post_type') == "follow":
            posts = posts.filter(Q(title__icontains=q_word) | Q(text__icontains=q_word)).order_by('-created_at')
        else:
            posts = Post.objects.filter(Q(title__icontains=q_word) | Q(text__icontains=q_word)).order_by('-created_at')
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
        messages.warning(request, 'ログインできませんでした')
    return render(request, 'groomings/login.html', context={
        'login_form': login_form
    })

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'ログアウトしました')
    return redirect('groomings:login')

def user_signup(request):
    """サインアップ画面"""
    form = forms.UserAddForm()
    if request.method == 'POST':
        form = forms.UserAddForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'ユーザーを登録しました')
                return redirect('groomings:login')
            except ValidationError as e:
                form.add_error('password', e) # formのパスワードの部分にエラー内容を追加
        messages.warning(request, '再入力してください')
    return render(request, 'groomings/signup.html', context={
        'form': form,
    })

@login_required
def user(request, user_id):
    """ユーザーページ"""
    user = User.objects.get(pk=user_id)
    my_follows = request.user.follow.all()
    posts = user.user_post.all()
    return render(request, 'groomings/user.html', context={"page_owner": user, "my_follows": my_follows, "posts": posts})

@login_required
def user_favo(request, user_id):
    """ユーザーのお気に入りした投稿一覧ページ"""
    user = User.objects.get(pk=user_id)
    my_follows = request.user.follow.all()
    favo_posts = user.user_favo_post.all()
    return render(request, 'groomings/user_favo.html', context={"page_owner": user, "my_follows": my_follows, 'favo_posts': favo_posts})

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
    """ユーザーパスワード編集ページ"""
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
    """投稿ページ"""
    form = forms.PostForm(request.POST or None, request.FILES or None)
    if form.is_valid(): # バリデーションがOKなら保存
        form.instance.user = request.user
        toukou = form.save()
        messages.info(request, f'投稿しました。ユーザー:{toukou.user} タイトル:{toukou.title} pk:{toukou.pk}')
        return redirect('groomings:top')
    return render(request, 'groomings/create_post.html', context={"form": form}) # , 'id': user_id})

def ranking(request):
    """ランキング用のページ"""
    users = User.objects.order_by('-point')
    post_orderby_favo = Post.objects.annotate(num_favo=Count('favorite')).order_by('-num_favo')[:10]
    return render(request, 'groomings/ranking.html',context={"users": users,"points":post_orderby_favo}) # , 'id': user_id})

@login_required
def post_detail(request, post_id):
    """投稿詳細ページ"""
    post = Post.objects.get(pk=post_id)
    comme_form = forms.CommentForm(request.POST or None)
    if comme_form.is_valid():
        if request.user.point > 40: # ログインユーザーのポイントが70より大きくなければコメントできない
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
    """匿名質問詳細ページ"""
    question = Question.objects.get(pk=question_id)
    question_users = [question.giver, question.recipient]
    if not request.user in question_users: # 匿名質問した人か答える人以外はtopへリダイレクト
        return redirect('groomings:top')
    rep_form = forms.ReplyForm(request.POST or None, request.FILES or None)
    if rep_form.is_valid():
        if request.user.point > 70 and question.recipient > 100:
            rep_form.instance.question = question
            rep_form.instance.giver = request.user
            if question.giver == request.user:
                rep_form.instance.recipient = question.recipient
            else:
                rep_form.instance.recipient = question.giver
            rep_form.save()
            messages.success(request, '返信しました')
            return redirect('groomings:question_detail', question_id=question.id)
        else:
            messages.warning('所持ポイントが足りません。もしくは回答者のポイントが足りていません')
    replys = question.question_reply.all()
    return render(request, 'groomings/question_detail.html', context={"question": question, "form": rep_form, "replys": replys})


@login_required
def follow(request, user_id):
    """フォローする"""
    follow_user = User.objects.get(pk=user_id)
    if request.user == follow_user:
        messages.warning(request, '自分自身はフォローできません')
        return redirect('groomings:top')
    elif follow_user in request.user.follow.all():
        messages.warning(request, 'すでにフォロー中のユーザーはフォローできません')
        return redirect('groomings:user', user_id=user_id)
    else:
        request.user.follow.add(follow_user)
        messages.success(request, f'{follow_user.username}をフォローしました')
        return redirect('groomings:user', user_id=user_id)

@login_required
def unfollow(request, user_id):
    """フォロー解除する"""
    unfollow_user = request.user.follow.all().filter(pk=user_id).first()
    if unfollow_user:
        request.user.follow.remove(unfollow_user)
        messages.success(request, f'{unfollow_user.username}のフォローを解除しました')
        return redirect('groomings:user', user_id=user_id)
    else:
        messages.warning(request, 'フォローしてないユーザーです')
        return redirect('groomings:user', user_id=user_id)

@login_required
def followee(request, user_id):
    """フォロー中ユーザー一覧"""
    user = User.objects.get(pk=user_id)
    my_follows = request.user.follow.all() # ログインユーザーがフォローしてるユーザーたち
    followees = user.follow.all() # user_idのユーザーがフォローしてるユーザーたち
    return render(request, 'groomings/follow.html', context={"page_owner": user, "my_follows": my_follows, "followees": followees})

@login_required
def follower(request, user_id):
    """フォロワー一覧"""
    user = User.objects.get(pk=user_id)
    my_follows = request.user.follow.all() # ログインユーザーがフォローしてるユーザーたち
    followers = user.follower.all() # useridのユーザーのフォロワーたち
    return render(request, 'groomings/follower.html', context={"page_owner": user, "my_follows": my_follows, "followers": followers})
    
@login_required
def favorite(request, post_id):
    """お気に入りとお気に入りの取り消し"""
    post = Post.objects.get(pk=post_id)
    if request.user in post.favorite.all():
        post.favorite.remove(request.user)
        if post.user.point >= 5:
            post.user.point -= 5 # いいねが取り消されたユーザーは5ポイントマイナスされる
            post.user.save()
        messages.success(request, '投稿へのいいねを取り消しました')
        return redirect('groomings:post_detail', post_id)
    else:
        post.favorite.add(request.user)
        post.user.point += 5 # いいねされたユーザーは5ポイントプラスされる
        post.user.save()
        messages.success(request, '投稿にいいねしました')
        return redirect('groomings:post_detail', post_id)

@login_required
def favo_comme(request, comment_id):
    """コメントへのお気に入りとお気に入りの取り消し"""
    comment = Comment.objects.get(pk=comment_id)
    if request.user in comment.favorite.all():
        comment.favorite.remove(request.user)
        if comment.user.point >= 5:
            comment.user.point -= 5
            comment.user.save()
        messages.success(request, 'コメントへのいいねを取り消しました')
        return redirect('groomings:post_detail', comment.post.id)
    else:
        comment.favorite.add(request.user)
        comment.user.point += 5
        comment.user.save()
        messages.success(request, 'コメントにいいねしました')
        return redirect('groomings:post_detail', comment.post.id)

@login_required
def bad_comme(request, comment_id):
    """コメントへのバッドとバッド取り消し"""
    comment = Comment.objects.get(pk=comment_id)
    if request.user in comment.bad.all():
        comment.bad.remove(request.user)
        comment.user.point += 5
        comment.user.save()
        messages.success(request, 'コメントへのバッドを取り消しました')
        return redirect('groomings:post_detail', comment.post.id)
    else:
        comment.bad.add(request.user)
        if comment.user.point >= 5:
            comment.user.point -= 5
            comment.user.save()
        messages.success(request, 'コメントにバッドしました')
        return redirect('groomings:post_detail', comment.post.id)
