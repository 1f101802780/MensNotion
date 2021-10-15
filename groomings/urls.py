from django.urls import path
from . import views

app_name = 'groomings'
urlpatterns = [
    path(r'', views.top, name = 'top'), # タイムライン
    path(r'login/', views.login, name = 'login'), # ログイン画面
    path(r'signup/', views.signup, name = 'signup'), # ユーザー登録画面
    path(r'user/<int:user_id>/', views.user, name = 'user'), # ユーザー個人ページ
    path(r'user/<int:user_id>/favo', views.user_favo, name='user_favo'), # ユーザーのお気に入り投稿ページ
    path(r'edit/user/<int:user_id>/', views.edit_user, name='edit_user'), # ユーザー情報編集ページ
    path(r'post/', views.create_post, name='create_post'), # post投稿ページ
    path(r'ranking/', views.ranking, name='ranking'),# ランキング用のページ
    # 匿名質問をするためのページ(<int:user_id>必要)
    # 投稿詳細ページ(<int:post_id>必要)
    # 匿名質問に関するページ(自分にきた質問と自分がした質問を表示)(<int:user_id>必要)
    # 自分がしたかされた匿名質問の詳細ページ(<int:question_id>必要)
]
