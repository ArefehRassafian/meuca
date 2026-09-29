from pathlib import Path
from uuid import uuid4

import jdatetime
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

id_validator = RegexValidator(
    regex=r"^@[a-zA-Z][a-zA-Z0-9_]{4,31}$",
    message="شماره تلفن باید 11 رقم باشد و با 09 شروع شود.",
)
phone_validator = RegexValidator(
    regex=r"^09\d{9}$",
    message="شماره تلفن باید 11 رقم باشد و با 09 شروع شود.",
)
def banner_image_upload_path(instance, filename):
    """
    برای جلوگیری از تداخل نام تصاویر، نام تصادفی تولید می‌کند.
    مثال:
    media/products/84e3b...jpg
    """
    extension = Path(filename).suffix.lower()
    return f"banner/{uuid4().hex}{extension}"
def blog_image_upload_path(instance, filename):
    """
    برای جلوگیری از تداخل نام تصاویر، نام تصادفی تولید می‌کند.
    مثال:
    media/products/84e3b...jpg
    """
    extension = Path(filename).suffix.lower()
    return f"blog/{uuid4().hex}{extension}"

# Create your models here.
class Setting(models.Model):
    about = models.TextField(
        max_length=1000,
        verbose_name="متن درباره ما"
    )
    phone = models.CharField(
        max_length=11,
        validators=[phone_validator],
        verbose_name='شماره تلفن'
    )
    id_tel = models.CharField(
        max_length=20,
        validators=[id_validator],
        verbose_name='آیدی تلگرام'
    )
    footer = models.CharField(
        max_length=100,
        verbose_name='متن پایین صفحه'
    )

    class Meta:
        verbose_name = "تنظیمات"
        verbose_name_plural = "تنظیمات"

    def __str__(self):
        return self.phone


class Questions(models.Model):
    setting = models.ForeignKey(
        Setting,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name="تنظیمات")
    question = models.CharField(max_length=300, verbose_name="متن سوال")
    answer = models.TextField(verbose_name="پاسخ سوال")
    class Meta:
        verbose_name = "سوال"
        verbose_name_plural = "سوال ها"

    def __str__(self):
        return self.question


class Rules(models.Model):
    setting = models.ForeignKey(
        Setting,
        on_delete=models.CASCADE,
        related_name="rules",
        verbose_name="تنظیمات"
    )
    rule = models.TextField(verbose_name="قانون")
    class Meta:
        verbose_name = "قانون"
        verbose_name_plural = "قوانین"

    def __str__(self):
        return self.rule


class ImageBanner (models.Model):
    setting = models.ForeignKey(
        Setting,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="تنظیمات"
    )
    image = models.ImageField(
        upload_to=banner_image_upload_path,
        verbose_name="تصویر بنر",
    )
    class Meta:
        verbose_name = "تصویر"
        verbose_name_plural = "تصاویر"
    def __str__ (self):
        if self.image:
            return self.image.url
        else:
            return self.setting.phone



class Blog (models.Model):
    title = models.CharField(max_length=100, verbose_name="عنوان بلاگ")
    text = models.TextField(verbose_name="متن بلاگ")
    author =models.CharField(max_length=100,verbose_name="نویسنده")
    created = models.DateTimeField(auto_now_add=True,verbose_name="ژمان ایجاد")
    updated = models.DateTimeField(auto_now=True, verbose_name="آخرین بروز رسانی")
    class Meta:
        verbose_name = "بلاگ"
        verbose_name_plural = "بلاگ ها"

    @property
    def updated_jalali(self):
        if not self.updated:
            return None

        local_dt = timezone.localtime(self.updated)

        jalali = jdatetime.datetime.fromgregorian(
            datetime=local_dt
        )

        return jalali.strftime("%Y/%m/%d - %H:%M")

    @property
    def created_jalali(self):
        if not self.created:
            return None

        local_dt = timezone.localtime(self.created)

        jalali = jdatetime.datetime.fromgregorian(
            datetime=local_dt
        )


        return jalali.strftime("%Y/%m/%d - %H:%M")
    def __str__(self):
        return self.title
class ImageBlog (models.Model):
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="تصاویر"
    )
    image = models.ImageField(
        upload_to=blog_image_upload_path,
        verbose_name="تصویر بلاگ",
    )
    class Meta:
        verbose_name = "تصویر"
        verbose_name_plural = "تصاویر"
    def __str__(self):
        if self.image:
            return self.image.url
        else:
            return self.blog.title