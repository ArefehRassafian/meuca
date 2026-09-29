from decimal import Decimal
from pathlib import Path
from uuid import uuid4

from django.conf import settings

from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,

)
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone

#for pictureeeeeeee:
# pip install pillow =>for image field is needed if error =>python -m pip install --upgrade pip

def product_image_upload_path(instance, filename):
    """
    برای جلوگیری از تداخل نام تصاویر، نام تصادفی تولید می‌کند.
    مثال:
    media/products/84e3b...jpg
    """
    extension = Path(filename).suffix.lower()
    return f"products/{uuid4().hex}{extension}"

# class category_manager(models.Manager):
#     def get_queryset(self):
#         return super(category_manager, self).get_queryset().filter(name='hi')
#     def counter(self):
#         return len(self.all())
#     def published(self):
#         return self.filter(published_at__isnull=False)
def categories_image_upload_path(instance, filename):
    """
    برای جلوگیری از تداخل نام تصاویر، نام تصادفی تولید می‌کند.
    مثال:
    media/products/84e3b...jpg
    """
    extension = Path(filename).suffix.lower()
    return f"categories/{uuid4().hex}{extension}"

class Category(models.Model):

    name = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="دسته‌بندی",
    )
    # ord=models.Manager();
    # custom = models.category_manager()
    # slug = models.SlugField(
    #     null=True,
    #     unique=True,
    #
    # )
    image = models.ImageField(
        upload_to=categories_image_upload_path,
        verbose_name="تصویر دسته بندی"
    )
    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"


    def __str__(self):
        return self.name
    # def save(self,*args,**kwargs):
    #     self.slug=slugify(self.name)
    #
    #     super(Category, self).save(*args,**kwargs)






class Product(models.Model):

    name = models.CharField(
        max_length=255,
        verbose_name="نام محصول",
    )
    # choice =(
    # ("a" , "A"),
    # ("b", "B"),
    # )
    code = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="کدمحصول",
        # help_text="876543",
        # db_column="code2",
        #editable= False,
        # choices=choice , default ="a"
        # unique_for_date="created_at",

    )


    price = models.DecimalField(
        max_digits=14,
        decimal_places=0,
        validators=[MinValueValidator(0)],
        verbose_name="مبلغ",
        help_text="مبلغ را به تومان وارد کنید.",
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ثبت'
    )

    categories = models.ManyToManyField(
        Category,

        related_name="products",
        verbose_name="دسته بندی ",
    )




    discount_percent = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        verbose_name="درصد تخفیف",
    )

    published_at = models.DateTimeField(
        verbose_name="زمان انتشار",
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name="زمان ساخت",
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_products",
        editable=False,
        verbose_name="کاربر ثبت‌کننده",
    )


    class Meta:
        verbose_name = "کالا"
        verbose_name_plural = "کالاها"
        ordering = ["-published_at"]
        constraints = [

            models.CheckConstraint(
                condition=Q(price__gte=0),
                name="product_price_gte_zero",
            ),
            models.CheckConstraint(
                condition=(
                    Q(discount_percent__isnull=True)
                    | Q(discount_percent__range=(0, 100))
                ),
                name="product_discount_between_zero_and_hundred",
            ),
        ]

    def get_absolute_url(self):
        return reverse("products:products_detail" , args=[self.id])


    @property
    def final_price(self):
        """مبلغ محصول بعد از اعمال تخفیف."""
        if not self.discount_percent:
            return self.price

        discount = Decimal(self.discount_percent)
        return self.price * (Decimal("100") - discount) / Decimal("100")


    def publish(self):
        return self.published_at<=timezone.now()

    publish.short_description="انتشار"
    #
    # def show_image (self):
    #     return format_html(f'<img src="{self.images.first().image.url}" width="50" height="50" >')
    #











    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="کالا"
    )

    image = models.ImageField(
        upload_to=product_image_upload_path,
        verbose_name="تصویر کالا"
    )

    def __str__(self):
        return f"تصویر {self.product}"

    class Meta:
        verbose_name = "تصویر کالا"
        verbose_name_plural = "تصاویر کالا"



