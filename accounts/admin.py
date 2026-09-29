from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import (
    User,
    Address, Message

)








# admin.site.site_header="مدیریت میوکا"
# =========================================================
# Address Inline
# نمایش آدرس‌های کاربر داخل صفحه مدیریت کاربر
# =========================================================

class AddressInline(admin.TabularInline):
    model = Address
    extra = 0
    fk_name = "user"

    fields = (
        "name",
        "province",
        "city",
        "address",
        "postal_code",

    )

    show_change_link = True


# =========================================================
# User Admin
# =========================================================

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [AddressInline]

    list_display = (
        "picture",
        "id",
        "username",
        "phone_number",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "date_joined",




    )

    list_display_links = (
        "id",
        "username",
    )

    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "date_joined",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
        "phone_number",
    )

    ordering = ("-date_joined",)





    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (
            "اطلاعات تکمیلی کاربر",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "phone_number",
                    "picture",
                )
            },
        ),
    )

    fieldsets = BaseUserAdmin.fieldsets + (
        ('اطلاعات تکمیلی کاربر', {
            'fields': ('picture',"phone_number")
        }),
    )


# =========================================================
# Address Admin
# =========================================================
admin.site.register(Message)

# @admin.register(PendingRegistration)
# class PendingRegistrationAdmin(admin.ModelAdmin):
#     list_display = (
#         "first_name",
#         "last_name",
#         "username",
#         "phone_number",
#         "created_at"
#     )
#     list_filter = ("created_at",)
#     search_fields = ("username", "phone_number", "first_name", "last_name")

# @admin.register(PasswordResetCode)
# class PasswordResetCodeAdmin(admin.ModelAdmin):
#     list_display = (
#         "user",
#         "code",
#         "created_at"
#     )
#     list_filter = ("created_at",)
#     search_fields = ("user__username" ,"user__phone_number" , "user__first_name","user__last_name")
