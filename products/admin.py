

from django.contrib import admin

from .models import (

    Category,
    Product,
ProductImage,
)

# class FilterByName (admin.SimpleListFilter):
#     title = "نام"
#     parameter_name = "name"
#     def lookups(self, request, model_admin):
#         return (
#         ("tools","اسباب بازی "),
#         ("food","غذا")
#         )
#     def queryset(self, request, queryset):
#         if self.value():
#             return queryset.filter(name__icontains=self.value())
#         return None


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ( "name",)
    search_fields = ("name",)

    @admin.display(description="عنوان")
    def title(self, obj):
        return obj.get_code_display()
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    min_num = 2
    validate_min = True

    fields = (
        "image",

    )




@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = (
        "name",
        "code",
        "price",
        "final_price_display",
        "created_by",
        "publish",
        "created_at"
    )


    list_filter = (
        "created_at",
        "categories",
        "published_at",
    )

    search_fields = (
        "name",
        "description",
        "code",
    )



    readonly_fields = (
        "created_by",
        "created_at",
        "final_price_display",
        "updated"

    )


    fieldsets = (
        (
            "اطلاعات اصلی",
            {
                "fields": (
                    "name",
                    "code",
                    "price",
                    "discount_percent",
                    "final_price_display",
                    "description",

                )
            },
        ),
        (
            "دسته‌بندی محصول",
            {
                "fields": (
                    "categories",

                )
            },
        ),

        (
            "اطلاعات سیستمی",
            {
                "fields": (

                    "created_by",
                    "created_at",
                    "published_at",
                    "updated"
                )
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        # فقط زمان ساخت محصول، کاربر ثبت‌کننده تعیین می‌شود.
        if not obj.pk:
            obj.created_by = request.user

        super().save_model(request, obj, form, change)

    @admin.display(description="مبلغ بعد از تخفیف")
    def final_price_display(self, obj):
        if not obj or not obj.pk:
            return "-"
        return obj.final_price




