from django.db.models.fields import EmailField
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from groomings.models import User, Post, Comment, Question, Reply, Tag, Notify
from django.contrib import messages
from django.db.models import Count
from django.db.models import Q
from datetime import datetime, timedelta
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.views.generic import TemplateView

def top(request):
    """トップ画面"""
    if request.user.is_authenticated: # ログインしていたらフォロー中ユーザーの投稿を表示
        users = request.user.follow.all()
        posts = Post.objects.filter(Q(user__in=users) | Q(user=request.user)).order_by('-created_at')
    else:
        posts = Post.objects.order_by('-created_at')
    return render(request, 'groomings/top.html', context={"posts": posts})

def search(request):
    posts = Post.objects.order_by('-created_at')
    all_tags = Tag.objects.all()
    check_tag_ids = []
    if request.GET.get('button') == "検索する":
        q_word = request.GET.get('query')
        if request.GET.get('category') == "all" :
            posts = posts.filter(Q(title__icontains=q_word) | Q(text__icontains=q_word)).order_by('-created_at')
        else:
            posts = posts.filter(Q(title__icontains=q_word) | Q(text__icontains=q_word), category=request.GET.get('category')).order_by('-created_at')
        check_tag_ids = request.GET.getlist("tag")
        check_tag_ids = [int(i) for i in check_tag_ids]
        for tag_id in check_tag_ids:
                posts = posts.filter(having_tags=tag_id).order_by('-created_at')

    return render(request, 'groomings/search.html', context={"posts": posts, "tags": all_tags, "check_tag_ids": check_tag_ids})

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
        form = forms.UserAddForm(request.POST, request.FILES)
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
    notifys = Notify.objects.filter(user=request.user).order_by('-created_at')
    eval_as_giver = user.user_give_question.filter(is_active=False).order_by('-created_at')
    eval_as_recipient = user.user_receive_question.filter(is_active=False).order_by('-created_at')
    return render(request, 'groomings/user.html', context={
        "page_owner": user, "my_follows": my_follows, "posts": posts, "notifys": notifys, "eval_as_giver": eval_as_giver, "eval_as_recipient": eval_as_recipient
        })

@login_required
def user_favo(request, user_id):
    """ユーザーのお気に入りした投稿一覧ページ"""
    user = User.objects.get(pk=user_id)
    my_follows = request.user.follow.all()
    favo_posts = user.user_favo_post.all()
    notifys = Notify.objects.filter(user=request.user).order_by('-created_at')
    eval_as_giver = user.user_give_question.filter(is_active=False).order_by('-created_at')
    eval_as_recipient = user.user_receive_question.filter(is_active=False).order_by('-created_at')
    return render(request, 'groomings/user_favo.html', context={
        "page_owner": user, "my_follows": my_follows, 'favo_posts': favo_posts, "notifys": notifys, "eval_as_giver": eval_as_giver, "eval_as_recipient": eval_as_recipient
        })

@login_required
def edit_user(request):
    """ユーザー情報編集ページ"""
    edit_user_form = forms.UserEditForm(request.POST or None, request.FILES or None, instance=request.user)
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
    tag_form = forms.TagForm(request.POST or None)
    tags = Tag.objects.all()

    if tag_form.is_valid():
        tag_form.save()
        return redirect('groomings:create_post')

    if form.is_valid(): # バリデーションがOKなら保存
        form.instance.user = request.user
        toukou = form.save()
        check_tag_ids = request.POST.getlist("tag")
        for tag_id in check_tag_ids:
            Tag.objects.get(pk=tag_id).post.add(toukou)

        messages.info(request, f'投稿しました。ユーザー:{toukou.user} タイトル:{toukou.title} pk:{toukou.pk}')
        return redirect('groomings:top')
    return render(request, 'groomings/create_post.html', context={"form": form, "tag_form": tag_form, "tags": tags})

def ranking(request):
    """ランキング用のページ"""
    points = User.objects.order_by('-point')[:10]
    follower = User.objects.annotate(num_follower=Count('follower')).order_by('-num_follower')[:10]
    num_que = User.objects.annotate(num_que=Count('user_receive_question')).order_by('-num_que')[:10]
    
    post_orderby_favo = Post.objects.annotate(num_favo=Count('favorite')).order_by('-num_favo')[:10]
    return render(request, 'groomings/ranking.html',context={"points": points, "followers": follower, "num_que": num_que, "goods": post_orderby_favo}) # , 'id': user_id})

@login_required
def post_detail(request, post_id):
    """投稿詳細ページ"""
    post = Post.objects.get(pk=post_id)
    comme_form = forms.CommentForm(request.POST or None)
    if comme_form.is_valid():
        if good_bad(request.user) > -10: # 1週間以内のコメントに対するbadがgood+10を上回るとコメできない
            comme_form.instance.user = request.user
            comme_form.instance.post = post
            comme_form.save()
            messages.success(request, 'コメントしました')
            return redirect('groomings:top')
        else:
            messages.warning(request, '週間bad数がgood数+10以上だとコメできません')
    unvisited_comme_notifys = Notify.objects.filter(kind="comment", notify_id=post_id, user=request.user, is_visited=False)
    for notify in unvisited_comme_notifys: # このポストについたコメントの通知をvisitedにする
        notify.is_visited = True
        notify.save()
    comments = post.post_comment.all()
    return render(request, 'groomings/post_detail.html', context={"post": post, "form": comme_form, "comments": comments})

def good_bad(user):
    my_commes = user.user_comment.all()
    week_commes = my_commes.filter(created_at__gte = datetime.now() - timedelta(weeks=1))
    num_good = 0
    num_bad = 0
    for comme in week_commes:
        num_good += comme.favorite.count()
        num_bad += comme.bad.count()
    return num_good - num_bad

@login_required
def post_edit(request, post_id):
    """投稿編集ページ"""
    post = request.user.user_post.all().filter(pk=post_id).first()
    if not post:
        return redirect('groomings:top')
    edit_post_form = forms.PostForm(request.POST or None, request.FILES or None, instance=post)
    tags = Tag.objects.all()
    if edit_post_form.is_valid():
        toukou = edit_post_form.save()
        check_tag_ids = request.POST.getlist("tag")
        toukou.having_tags.set(check_tag_ids)
        messages.success(request, '投稿を更新しました')
    return render(request, 'groomings/edit_post.html', context={"edit_post_form": edit_post_form, "tags": tags, "post": post})

@login_required
def post_delete(request, post_id):
    """投稿削除"""
    post = request.user.user_post.all().filter(pk=post_id).first()
    if not post:
        return redirect('groomings:top')
    post.delete()
    notifys = Notify.objects.filter(kind="comment", notify_id=post_id)
    for notify in notifys:
        notify.delete()
    messages.success(request, '投稿が削除されました')
    return redirect('groomings:top')

@login_required
def create_question(request, user_id):
    """匿名質問を送るページ"""
    recipient = User.objects.get(pk = user_id)
    if recipient.point < 20 or request.user.point < 20:
        messages.warning(request, '相手または自分の所持ポイントが足りません')
        return redirect('groomings:top')
        
    form = forms.QuestionForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.instance.recipient = recipient
        form.instance.giver = request.user
        form.save()
        request.user.point -= form.instance.give_point
        messages.success(request, f'{form.instance.give_point}を使って質問しました')
        return redirect('groomings:top')
    return render(request, 'groomings/create_question.html', context={"form": form, "recipient": recipient})


@login_required
def question_detail(request, question_id):
    """匿名質問詳細ページ"""
    question = Question.objects.get(pk=question_id)
    question_users = [question.giver, question.recipient]
    if not request.user in question_users: # 匿名質問した人か答える人以外はtopへリダイレクト
        return redirect('groomings:top')
    rep_form = forms.ReplyForm(request.POST or None, request.FILES or None)
    if question.is_active == True:
        if rep_form.is_valid():
            rep_form.instance.question = question
            rep_form.instance.giver = request.user
            if question.giver == request.user:
                rep_form.instance.recipient = question.recipient
            else:
                rep_form.instance.recipient = question.giver
            rep_form.save()
            messages.success(request, '返信しました')
            return redirect('groomings:question_detail', question_id=question.id)

        if request.POST.get("button") == "評価する":
            if question.recipient == request.user and question.to_giver_point == None: # 自分が回答者の場合
                question.to_giver_point = int(request.POST.get("eval"))
                if question.giver:
                    Notify.objects.create(kind="togiver_eval", notify_id=question_id, user=question.giver, from_user=question.recipient)
                question.save()
                messages.success(request, '質問者を評価しました')
            elif question.giver == request.user and question.to_recipient_point == None: # 自分が質問者の場合
                question.to_recipient_point = int(request.POST.get("eval"))
                if question.recipient:
                    Notify.objects.create(kind="torecipient_eval", notify_id=question_id, user=question.recipient, from_user=question.giver)
                question.save()
                messages.success(request, '回答者を評価しました')
            else:
                messages.warning(request, "既に評価済みです")

            if question.to_giver_point and question.to_recipient_point: # 両方評価したら質問をclose
                question.is_active = False
                question.save()
                if question.recipient:
                    question.recipient.point += (question.give_point - 5) # 質問者が付与したポイントから消滅分5ポイントを引いた分が回答者に入る
                    question.recipient.point += question.to_recipient_point # さらに質問者からの評価のポイントが追加
                    question.recipient.save()
                if question.giver:
                    question.giver.point += question.to_giver_point # 回答者からの評価のポイントが追加
                    question.giver.save()
            return redirect('groomings:question_detail', question_id)

    unvisited_que_rep_notifys = Notify.objects.filter(kind__in=["question", "reply", "togiver_eval", "torecipient_eval"], notify_id=question_id, user=request.user, is_visited=False)
    for notify in unvisited_que_rep_notifys: # 匿名質問とリプライの通知をvisitedにする
        notify.is_visited = True
        notify.save()
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
    notifys = Notify.objects.filter(user=request.user).order_by('-created_at')
    eval_as_giver = user.user_give_question.filter(is_active=False).order_by('-created_at')
    eval_as_recipient = user.user_receive_question.filter(is_active=False).order_by('-created_at')
    return render(request, 'groomings/follow.html', context={
        "page_owner": user, "my_follows": my_follows, "followees": followees, "notifys": notifys, "eval_as_giver": eval_as_giver, "eval_as_recipient": eval_as_recipient
        })

@login_required
def follower(request, user_id):
    """フォロワー一覧"""
    user = User.objects.get(pk=user_id)
    my_follows = request.user.follow.all() # ログインユーザーがフォローしてるユーザーたち
    followers = user.follower.all() # useridのユーザーのフォロワーたち
    notifys = Notify.objects.filter(user=request.user).order_by('-created_at')
    eval_as_giver = user.user_give_question.filter(is_active=False).order_by('-created_at')
    eval_as_recipient = user.user_receive_question.filter(is_active=False).order_by('-created_at')
    return render(request, 'groomings/follower.html', context={
        "page_owner": user, "my_follows": my_follows, "followers": followers, "notifys": notifys, "eval_as_giver": eval_as_giver, "eval_as_recipient": eval_as_recipient
        })
    
@login_required
def favorite(request, post_id):
    """お気に入りとお気に入りの取り消し"""
    post = Post.objects.get(pk=post_id)
    if request.user in post.favorite.all():
        post.favorite.remove(request.user)
        messages.success(request, '投稿へのいいねを取り消しました')
        return redirect('groomings:post_detail', post_id)
    else:
        post.favorite.add(request.user)
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

@login_required
def Anyms(request, user_id):
    """匿名質問に関するページ"""
    user = User.objects.get(pk=user_id)
    givequestion = user.user_give_question
    receive = user.user_receive_question
    return render()