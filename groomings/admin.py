from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .forms import UserChangeForm, UserAddForm

# Register your models here.
User = get_user_model()

class CustomizeUserAdmin(UserAdmin):
    form = UserChangeForm  # ユーザ編集画面で使うフォーム
    add_form = UserAddForm  # ユーザ作成画面
    
    # 一覧画面で表示する
    list_display = ('username', 'email', 'point', 'is_staff')


    # ユーザ編集画面で表示する要素
    fieldsets = (
        ('ユーザ情報', {'fields': ('username', 'email', 'password')}),
        ('パーミッション', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )

    add_fieldsets = (
        ('ユーザ情報', {
            'fields': ('username', 'email', 'password', 'confirm_password')
        }),
    )

admin.site.register(User, CustomizeUserAdmin)