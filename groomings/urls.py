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
    # path(r'post',views.post, name='POST'),
    path(r'post/', views.list_create, name='list_create'), # post投稿ページ
]
