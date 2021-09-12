from django.urls import path
from . import views

app_name = 'groomings'
urlpatterns = [
    path(r'', views.top, name = 'top'),
    path(r'login/', views.login, name = 'login'),
    path(r'signup/', views.signup, name = 'signup'),
    path(r'user/<int:user_id>/', views.user, name = 'user'),
    path(r'user/<int:user_id>/favo', views.user_favo, name='user_favo'),
    path(r'edit/user/<int:user_id>/', views.edit_user, name='edit_user'),
]
