from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile
from .forms import MyUserChangeForm, MyUserCreationForm, ProfileAdminForm

from django.utils.translation import gettext_lazy as _


# adminサイトのタイトル変更
admin.site.site_title = 'タイトルタグ'
admin.site.site_header = 'OGLeague'
admin.site.index_title = 'メニュー'



class ProfileAdminInline(admin.StackedInline):
    model = Profile
    can_delete = False
    form = ProfileAdminForm


# Register your models here.
@admin.register(User)
class MyUserAdmin(UserAdmin):
    change_user_password_template = None
    fieldsets = (
        (None,
            {
                "fields":(
                    "username", "account_name", "email", "password",
                ),
            }
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": (
                    "wide",
                    "collapse",
                ),
            },
        ),
        (
            _("Important dates"),
            {
                "fields": (
                    "last_login", "date_joined",
                ),
                "classes": (
                    "wide",
                    "collapse",
                ),
            }
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "account_name", "email", "password1", "password2"),
            },
        ),
    )
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ("username", "account_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "account_name", "email")
    ordering = ("username", "account_name", )
    inlines = [ProfileAdminInline]