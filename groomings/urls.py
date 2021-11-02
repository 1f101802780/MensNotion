from django.urls import path
from . import views

app_name = 'groomings'
urlpatterns = [
    path(r'', views.top, name = 'top'), # タイムライン
    path(r'login/', views.user_login, name = 'login'), # ログイン画面
    path(r'logout/', views.user_logout, name = 'logout'), #ログアウト用
    path(r'signup/', views.user_signup, name = 'signup'), # ユーザー登録画面
    path(r'user/<int:user_id>/', views.user, name = 'user'), # ユーザー個人ページ
    path(r'user/<int:user_id>/favo', views.user_favo, name='user_favo'), # ユーザーのお気に入り投稿ページ
    path(r'edit_user/', views.edit_user, name='edit_user'), # ユーザー情報編集ページ
    path(r'change_password/', views.change_password, name='change_password'),
    path(r'post/', views.create_post, name='create_post'), # post投稿ページ
    path(r'ranking/', views.ranking, name='ranking'), # ランキング用のページ
    # 匿名質問をするためのページ(<int:user_id>必要)
    path(r'post/<int:post_id>/', views.post_detail, name='post_detail'), # 投稿詳細ページ(<int:post_id>必要)
    # 匿名質問に関するページ(自分にきた質問と自分がした質問を一覧表示)(<int:user_id>必要)
    path(r'question/<int:question_id>/', views.question_detail, name='question_detail'), # 自分がしたかされた匿名質問の詳細ページ(<int:question_id>必要)
    path(r'follow/<int:user_id>/', views.follow, name='follow'), # フォロー用のurl
    path(r'unfollow/<int:user_id>/', views.unfollow, name='unfollow'), # フォロー解除用のurl
    path(r'followee/<int:user_id>/', views.followee, name='followee'), # フォローしてるユーザー一覧ページ
    path(r'follower/<int:user_id>/', views.follower, name='follower'), # フォロワーの一覧ページ
    path(r'favorite/<int:post_id>/', views.favorite, name='favorite'), # 投稿へのいいねあるいはいいねの取り消し用url
]
