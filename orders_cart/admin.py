from django.contrib import admin
from .models import Order, OrderItem



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = (
        'product',
        'quantity',
        'price',
        'discount_percent',

    )
    readonly_fields = (

        'price_all',
        'price_with_dis_all',

    )




@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'status',
        'is_paid',
        'payment_time_jalali',
        'updated_at_jalali',
        'created_at',
        'tracking_code',
        'receiver_name',
        'total_quantity',
        'tax_percent',
        'shipping_cost',
        'final_price'




    ]
    list_filter = (
        "created_at",
        'is_paid',
        'updated_at',
        'payment_time',

    )

    search_fields = (
        "items__product__name",
        "items__product__description",
        "user__phone_number",
        "user__username",
        "user__email",
        "user__last_name",
        "user__first_name",

    )

    readonly_fields = (
        'total_price_with_dis',
        'total_price',
        'total_quantity',
        'created_at',
        'tracking_code',
        'updated_at',
        'updated_at_jalali',
        'payment_time_jalali',
        'tax_percent',
        'shipping_cost',
        'final_price',
        'is_paid',



    )
    fieldsets = (
        (
            "کاربر",
            {
                "fields": (
                    "user",
                    "email",
                    'address',
                    "receiver_name",
                    'receiver_phone',

                )
            },
        ),
        (
            "اطلاعات سیستمی",
            {
                "fields": (

                    "created_at",
                    'updated_at_jalali',
                    'payment_time_jalali',
                    'total_price',
                    'total_price_with_dis',
                    'total_quantity',
                    'tracking_code',
                    'tax_percent',
                    'shipping_cost',
                    'final_price',


                )
            },
        ),
        (
            "وضعیت",
            {
                "fields": (

                    'status',
                    'is_paid',

                )
            },
        ),
    )
    inlines = [OrderItemInline]





# class CartItemInline(admin.TabularInline):
#     model = CartItem
#     extra = 1
#     fields = (
#         'product',
#         'quantity',
#         'price',
#         'price_with_dis',
#     )
#     readonly_fields = (
#         'price',
#         'price_with_dis'
#     )
#
#
#
#
#
# @admin.register(Cart)
# class CartAdmin(admin.ModelAdmin):
#
#     list_display = [
#         'id',
#         'user',
#         'created_at',
#         'updated_at',
#         'total_quantity',
#         'total_price',
#         'total_price_with_dis',
#         'total_price_with_dis_and_send'
#
#     ]
#     list_filter = (
#         "created_at",
#         "updated_at"
#     )
#
#     search_fields = (
#         "items__product__name",
#         "items__product__description",
#         "user",
#
#     )
#
#     readonly_fields = (
#         'total_price_with_dis_and_send',
#         'total_price_with_dis',
#         'total_price',
#         'total_quantity',
#         'created_at',
#         'updated_at',
#     )
#     fieldsets = (
#         (
#             "کاربر",
#             {
#                 "fields": (
#                     "user",
#                 )
#             },
#         ),
#         (
#             "اطلاعات سیستمی",
#             {
#                 "fields": (
#
#                     "created_at",
#                     "updated_at",
#                     'total_price',
#                     'total_price_with_dis',
#                     'total_price_with_dis_and_send',
#                     'total_quantity',
#
#                 )
#             },
#         ),
#     )
#
#     inlines = [
#         CartItemInline
#     ]
#
#

