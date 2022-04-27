from django.urls import path

from . import views


app_name = 'common'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('signup/', views.UserCreate.as_view(), name='signup'),
    path('signup/done/', views.UserCreateDone.as_view(), name='signup_done'),
    path('signup/complete/<str:token>/', views.UserCreateComplete.as_view(), name='signup_complete'),
    path('settings/', views.UserSettingsList.as_view(), name='user_settings_list'),
    path('settings/update/', views.user_settings_update, name='user_settings_update'),
    path('password/change/', views.PasswordChange.as_view(), name='password_change'),
    path('password/change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    path('password/reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('password/reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    path('password/reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password/reset/complete/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('email/change/', views.EmailChange.as_view(), name='email_change'),
    path('email/change/done/', views.EmailChangeDone.as_view(), name='email_change_done'),
    path('email/change/complete/<str:token>/', views.EmailChangeComplete.as_view(), name='email_change_complete'),
    path('users/', views.UserList.as_view(), name='user_list'),
    path('users/<username>/', views.UserDetail.as_view(), name='user_detail'),

    path('api/icon-upload/', views.api.icon_upload, name='api_icon_upload'),
]