from django.urls import path
from . import views

app_name = 'groomings'
urlpatterns = [
    path(r'', views.top, name = 'top'), # タイムライン
    path(r'login/', views.user_login, name = 'login'), # ログイン画面
    # ログアウト用のurl
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
]
