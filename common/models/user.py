from django.apps import apps
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from django.core.validators import RegexValidator, EmailValidator
from django.utils.translation import gettext_lazy as _


# Create your models here.
@deconstructible
class UsernameValidator(RegexValidator):
    regex = r'^(?!_)[a-zA-Z0-9_]{4,15}$'
    message = [
        'ユーザー名の長さは4文字以上15文字以下にする必要があります。',
        'ユーザー名に使えるのは、半角英数字（文字A～Z、数字0～9）、アンダースコア（_）のみです。スペースを含めることはできません。',
        'アンダースコア（_）から始めることはできません。'
    ]


@deconstructible
class AccountnameValidator(RegexValidator):
    regex = r'^(?!\s).{1,10}$'
    message = [
        'アカウント名の長さは1文字以上10文字以下にする必要があります。',
        'アカウント名にはひらがなやカタカナ、漢字、英数字（文字A～Z、数字0～9）、絵文字などを利用できます。',
        '空白文字から始めることはできません。',
    ]


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, account_name, email, password, **extra_fields):
        """
        Create and save a user with the given username, account_name, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        if not account_name:
            raise ValueError("The given account_name must be set")
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        account_name = self.model.normalize_username(account_name)
        user = self.model(username=username, account_name=account_name, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, account_name, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, account_name, email, password, **extra_fields)

    def create_superuser(self, username, account_name, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, account_name, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    AbstractUserをコピペして編集する
    """

    username_validator = UsernameValidator()
    account_name_validator = AccountnameValidator()
    email_validator = EmailValidator()

    username = models.CharField(
        _("ユーザー名"),
        max_length=15,
        unique=True,
        help_text=_(
            '4文字以上15文字以下にする必要があります。'
            '半角英数字とアンダースコア（_）のみです。スペースを含めることはできません。'
            'アンダースコア（_）から始めることはできません。'
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    account_name = models.CharField(
        _('アカウント名'),
        validators=[account_name_validator],
        max_length=10,
        help_text=_('10文字以下にする必要があります。'),
    )
    email = models.EmailField(
        _("email address"),
        validators=[email_validator],
        unique=True,
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['account_name', "email"]

    class Meta:
        verbose_name = _("ユーザー")
        verbose_name_plural = _("ユーザー")
        ordering = ['username', ]
        abstract = False

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)
        self.account_name = self.normalize_username(self.account_name)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
