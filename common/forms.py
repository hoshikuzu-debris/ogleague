from django import forms
from django.forms import ModelForm
from django.contrib import messages
from django.contrib.auth.forms import (
    AuthenticationForm, UserChangeForm, UserCreationForm,
    PasswordResetForm, SetPasswordForm, PasswordChangeForm
)
from django.contrib.auth import get_user_model, password_validation
from django.contrib.admin.widgets import AdminTextareaWidget
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from common.models import Profile

User = get_user_model()


"""
バリデーションが実行される順番は
1. Form.is_valid()
2. Form.フィールドに定義されたバリデーション
    文字種チェックなど
    フォームクラスに定義した順に実行される
3. Form.clean_<フィールド名>()
    単項目。フィールド単体のバリデーション。
    妥当性チェック
    フォームクラスに定義した順に実行される
4. Form.clean() ~= Form.clean_form()
    複数項目,複数項目
    データベースとの整合性チェック
5. Fom.post_clean()
6. バリデーション OK の場合、 Form.cleaned_data に検証済みデータがセットされる
    is_valid() 未実行の場合は cleaned_data 属性自体が存在しない
"""



class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class LoginForm(AuthenticationForm):
    """ログインフォーム"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix = ""



class MyUserCreationForm(UserCreationForm):
    '''ユーザー登録用フォーム'''
    class Meta:
        model = User
        fields = ['username', 'account_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix = ""

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username, is_active=False).delete()
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("同じユーザー名が既に登録済みです。")

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email, is_active=False).delete()
        except User.DoesNotExist:
            return email
        raise forms.ValidationError("同じメールアドレスが既に登録済みです。")

    def _post_clean(self):
        """パスワードのバリデーションエラーをpassword2ではなくてpassword1に入れる"""
        super(forms.ModelForm, self)._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get("password2")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password2", error)


class UserUpdateForm(forms.ModelForm):
    '''ユーザー情報更新フォーム'''

    class Meta:
        model = User
        fields = ['username', 'account_name',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix = ""


class ProfileUpdateForm(forms.ModelForm):
    '''ユーザープロフィール情報更新フォーム'''

    class Meta:
        model = Profile
        fields = ['bio',]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': '3'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix = ""


# 管理サイト用のAnswerForm
class ProfileAdminForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'bio': AdminTextareaWidget(),
        }


class MySetPasswordForm(forms.Form):
    """
    パスワード再設定用フォーム(パスワード忘れて再設定)
    A form that lets a user change set their password without entering the old
    password
    """

    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix = ""


    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages["password_mismatch"],
                    code="password_mismatch",
                )
        password_validation.validate_password(password2, self.user)
        return password2

    """
    def clean(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            error =  ValidationError(
                    self.error_messages["password_mismatch"],
                    code="password_mismatch",
                )
            self.add_error('new_password1', error)
            self.add_error('new_password2', error)
        return super().clean()
    """

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class MyPasswordChangeForm(MySetPasswordForm):
    """
    パスワード変更フォーム
    A form that lets a user change their password by entering their old
    password.
    """

    error_messages = {
        **MySetPasswordForm.error_messages,
        "password_incorrect": _(
            "Your old password was entered incorrectly. Please enter it again."
        ),
    }
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True}
        ),
    )

    field_order = ["old_password", "new_password1", "new_password2"]

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise ValidationError(
                self.error_messages["password_incorrect"],
                code="password_incorrect",
            )
        return old_password


class MyPasswordResetForm(PasswordResetForm):
    """
    パスワード忘れたときのフォーム
    メールアドレスの入力フォームが表示される
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix = ""


class EmailChangeForm(forms.ModelForm):
    """メールアドレス変更フォーム"""
    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix = ""

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email, is_active=False).delete()
        except User.DoesNotExist:
            return email
        raise forms.ValidationError("同じメールアドレスが既に登録済みです。")
