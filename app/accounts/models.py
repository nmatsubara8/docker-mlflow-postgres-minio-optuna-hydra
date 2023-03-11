from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _


class MSYSUserRole(models.IntegerChoices):
    ROOT = 0
    ADMIN = 1
    STAFF = 2


class MSYSUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError("Emailを入力して下さい")
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        # extra_fields.setdefault("role", MSYSUserRole.STAFF)
        extra_fields.setdefault("is_admin", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        # extra_fields.setdefault("role", MSYSUserRole.ROOT)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)
        # if extra_fields.get("role") is not MSYSUserRole.ROOT:
        #     raise ValueError("role=ROOTである必要があります。")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("is_superuser=Trueである必要があります。")
        return self._create_user(username, email, password, **extra_fields)


class MSYSUser(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(_("username"), max_length=50, validators=[username_validator], blank=False)
    email = models.EmailField(
        _("email"),
        max_length=255,
        unique=True,
    )
    company = models.CharField(_("company"), max_length=50, blank=True)
    role = models.IntegerField(_("user role"), choices=MSYSUserRole.choices, default=MSYSUserRole.STAFF)  # enumを指定

    # 以下の２つは必須
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MSYSUserManager()

    # USERNAME_FIELDで指定したフィールドは、ログイン認証やメール送信などで利用します。unique=Trueの必要あり
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"  # ターミナルでユーザー作成（manage.py createsuperuser）するときに表示される項目です。複数指定可

    # 管理コマンドcreatesuperuserでユーザーを作成する際に入力が求められるフィールド名のリストです。
    # REQUIRED_FIELDS は Django の他の部分、例えば admin でのユーザ作成 には何の影響も与えません。
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """is_staff という属性であくせすできる必要がある"""
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
