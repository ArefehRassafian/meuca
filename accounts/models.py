from pathlib import Path
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    RegexValidator,
)
from django.db import models


def banner_image_upload_path(instance, filename):
    """
    برای جلوگیری از تداخل نام تصاویر، نام تصادفی تولید می‌کند.
    مثال:
    media/products/84e3b...jpg
    """
    extension = Path(filename).suffix.lower()
    return f"banner/{uuid4().hex}{extension}"
def accounts_image_upload_path(instance, filename):
    """
    برای جلوگیری از تداخل نام تصاویر، نام تصادفی تولید می‌کند.
    مثال:
    media/products/84e3b...jpg
    """
    extension = Path(filename).suffix.lower()
    return f"accounts/{uuid4().hex}{extension}"


# class cate
# Validators
# =========================================================

phone_validator = RegexValidator(
    regex=r"^09\d{9}$",
    message="شماره تلفن باید 11 رقم باشد و با 09 شروع شود.",
)

postal_code_validator = RegexValidator(
    regex=r"^\d{10}$",
    message="کدپستی باید10 رقم باشد.",
)


# =========================================================
# User
# =========================================================

class User(AbstractUser):

    picture = models.ImageField(
        upload_to=accounts_image_upload_path,
        null=True,
        blank=True,
        verbose_name="تصویر کاربر",


    )
    email = models.EmailField(
        verbose_name="ایمیل",
        null=True,
        blank=True,

    )
    phone_number = models.CharField(
        max_length=11,
        unique=True,
        validators=[phone_validator],
        verbose_name="شماره تلفن",

    )

    def __str__(self):
        full_name = self.get_full_name()
        if full_name:
            return f"{full_name} - {self.username}"
        return self.username

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"


# =========================================================
# Address
# =========================================================

class Address(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        #or SET_NULL with null=true
        #or SET_DEFAULT whit default =...
        #or PROTECT
        #or Do_NOTHING
        related_name="addresses",
        verbose_name="کاربر",
    )
    name =models.CharField(
        max_length=30,
        verbose_name="نام"
    )

    province = models.CharField(
        max_length=100,
        verbose_name="استان",
    )

    city = models.CharField(
        max_length=100,
        verbose_name="شهر",
    )

    address = models.TextField(
        max_length=1000,
        verbose_name="آدرس کامل",
    )

    postal_code = models.CharField(
        max_length=10,
        validators=[postal_code_validator],
        verbose_name="کد پستی",
    )



    def __str__(self):
        return f"{self.user} - {self.province}- {self.city}- {self.address}"

    class Meta:
        verbose_name = "آدرس "
        verbose_name_plural = "آدرس ها"
        ordering = ["-id"]



class Message(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="کاربر ارسال کننده"

    )
    title =models.CharField(
        max_length=100,
        verbose_name="عنوان"
    )
    text = models.TextField(
        max_length=1000,
        verbose_name="متن پیام"
    )
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "پیام"
        verbose_name_plural = "پیام ها"
        ordering = ["-id"]

# class PendingRegistration(models.Model):
#     username = models.CharField(max_length=150)
#     first_name = models.CharField(max_length=150, blank=True)
#     last_name = models.CharField(max_length=150, blank=True)
#
#     phone_number=models.CharField(max_length=11)
#
#     # پسورد اینجا خام ذخیره نمی‌شود؛
#     # RegisterForm خودش آن را hash می‌کند.
#     password = models.CharField(max_length=128)
#
#     code = models.CharField(max_length=6)
#
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def str(self):
#         return f"{self.username} - {self.email}"
#
#     class Meta:
#         verbose_name = "ثبت نام موقت"
#         verbose_name_plural = "ثبت نام های موقت"
#         ordering = ["-created_at"]

#
# class PasswordResetCode(models.Model):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="password_reset_codes",
#         verbose_name="کاربر",
#     )
#
#     code = models.CharField(
#         max_length=6,
#         verbose_name="کد تأیید",
#     )
#
#     created_at = models.DateTimeField(
#         auto_now_add=True,
#         verbose_name="زمان ایجاد",
#     )
#
#     def str(self):
#         return f"{self.user.phone_number} - {self.code}"
#
#     class Meta:
#         verbose_name = "کد فراموشی رمز"
#         verbose_name_plural = "کدهای فراموشی رمز"
#         ordering = ["-created_at"]

