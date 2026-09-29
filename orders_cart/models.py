import jdatetime
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings
import uuid

from django.utils import timezone

from products.models import Product
from accounts.models import Address

phone_validator = RegexValidator(
    regex=r"^09\d{9}$",
    message="شماره تلفن باید 11 رقم باشد و با 09 شروع شود.",
)


class Order(models.Model):
    STATUS_CHOICES = [
        ('waiting_payment', 'در انتظار پرداخت'),
        ('awaiting_approval', 'پرداخت شده و در انتظار تایید'),
        ('sending', 'در حال ارسال'),
        ('returned', 'بازگشتی'),
        ('cancelled', 'کنسل شده'),
        ('delivered', 'تحویل داده شد'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name='کاربر'
    )

    email = models.EmailField(

    )

    address = models.TextField(
        verbose_name='آدرس'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ثبت و پرداخت '
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='sending',
        verbose_name='وضعیت سفارش'
    )
    payment_time =models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="تاریخ ثبت و پرداخت"
    )

    tracking_code = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        verbose_name='کد پیگیری'
    )

    updated_at = models.DateTimeField(auto_now=True)

    receiver_name = models.CharField(
        max_length=100,
        verbose_name='نام گیرنده'
    )

    receiver_phone = models.CharField(
        max_length=20,
        validators=[phone_validator],
        verbose_name='شماره تلفن گیرنده'
    )
    is_paid = models.BooleanField(
        default=False,
        verbose_name="پرداخت"
    )

    shipping_cost = models.PositiveIntegerField(
        default=50000,
        verbose_name='هزینه ارسال'
    )

    tax_percent = models.PositiveSmallIntegerField(
        default=10,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        verbose_name='درصد مالیات'
    )

    final_price = models.PositiveIntegerField(
        default=0,
        verbose_name='قیمت نهایی'
    )

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش ها'
        ordering = ('-payment_time',)


    @property
    def updated_at_jalali(self):
        if not self.updated_at:
            return None

        local_dt = timezone.localtime(self.updated_at)

        jalali = jdatetime.datetime.fromgregorian(
            datetime=local_dt
        )

        return jalali.strftime("%Y/%m/%d - %H:%M")

    @property
    def payment_time_jalali(self):
        if not self.payment_time:
            return None

        local_dt = timezone.localtime(self.payment_time)

        jalali = jdatetime.datetime.fromgregorian(
            datetime=local_dt
        )

        return jalali.strftime("%Y/%m/%d - %H:%M")
    @property
    def total_price_with_dis(self):
        total = 0

        for item in self.items.all():
            total += item.price_with_dis_all

        return total

    @property
    def total_price(self):
        total = 0
        for item in self.items.all():
            total += item.price_all
        return total

    @property
    def total_quantity(self):
        total = 0

        for item in self.items.all():
            total += item.quantity

        return total

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


    def calculate_final_price(self):
        """
        محاسبه قیمت نهایی سفارش
        بعد از اینکه OrderItemها ساخته شده‌اند.
        """

        subtotal = self.total_price_with_dis

        tax = subtotal * self.tax_percent / 100

        self.final_price = (
                subtotal
                + tax
                + self.shipping_cost
        )

        return self.final_price

    def update_final_price(self):
        """
        محاسبه و ذخیره قیمت نهایی سفارش
        """

        self.calculate_final_price()

        super().save(
            update_fields=["final_price"]
        )

    def __str__(self):
        return f"Order {self.tracking_code}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="سفارش"
    )

    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name='محصول'
    )

    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='تعداد'
    )

    price = models.PositiveIntegerField(
        verbose_name="قیمت بدون احتساب تخفیف",
    )

    discount_percent = models.PositiveSmallIntegerField(

        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        verbose_name="درصد تخفیف",
    )

    class Meta:
        verbose_name = 'آیتم سفارش'
        verbose_name_plural = 'آیتم های سفارش'

    @property
    def price_all(self):
        if self.price is None or self.quantity is None:
            return 0

        return self.price * self.quantity

    @property
    def price_with_dis_all(self):
        price = self.price or 0
        discount = self.discount_percent or 0
        quantity = self.quantity or 0

        return (price - (discount * price / 100)) * quantity


    def __str__(self):
        return self.product.code

#
# class Cart(models.Model):
#
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='cart',
#         verbose_name='کاربر'
#     )
#
#     created_at = models.DateTimeField(
#         auto_now_add=True,
#         verbose_name='تاریخ ایجاد'
#     )
#
#     updated_at = models.DateTimeField(
#         auto_now=True,
#         verbose_name='آخرین تغییر'
#     )
#
#
#     class Meta:
#         verbose_name = 'سبد خرید'
#         verbose_name_plural = 'سبدهای خرید'
#
#     @property
#     def total_price(self):
#         total = 0
#
#         for item in self.items.all():
#             total += item.price
#
#         return total
#
#     @property
#     def total_price_with_dis(self):
#         total = 0
#
#         for item in self.items.all():
#             total += item.price_with_dis
#
#         return total
#
#     @property
#     def total_price_with_dis_and_send(self):
#         total =self.total_price_with_dis + 100000
#         return total
#
#     @property
#     def total_quantity(self):
#         total = 0
#
#         for item in self.items.all():
#             total += item.quantity
#
#         return total
#
#
#     def __str__(self):
#         return f"سبد خرید {self.user}"
# class CartItem(models.Model):
#
#     cart = models.ForeignKey(
#         Cart,
#         on_delete=models.CASCADE,
#         related_name='items',
#         verbose_name='سبد خرید'
#     )
#
#
#     product = models.ForeignKey(
#         'products.Product',
#         on_delete=models.CASCADE,
#         verbose_name='محصول'
#     )
#
#
#     quantity = models.PositiveIntegerField(
#         default=1,
#         verbose_name='تعداد'
#     )
#
#
#     added_at = models.DateTimeField(
#         auto_now_add=True,
#         verbose_name='تاریخ اضافه شدن'
#     )
#
#
#     class Meta:
#         verbose_name = 'آیتم سبد خرید'
#         verbose_name_plural = 'آیتم های سبد خرید'
#
#         constraints = [
#             models.UniqueConstraint(
#                 fields=[
#                     'cart',
#                     'product'
#                 ],
#                 name='unique_product_in_cart'
#             )
#         ]
#
#     @property
#     def price(self):
#         return self.product.price * self.quantity
#     @property
#     def price_with_dis(self):
#         return self.product.final_price * self.quantity
#
#
#
#     def __str__(self):
#         return self.product.name


