from django.urls import path
from . import views

app_name = 'groomings'
urlpatterns = [
    path(r'', views.top, name = 'top'),
    path(r'login', views.login, name = 'login')
]
