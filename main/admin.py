from django.contrib import admin
from .models import Questions,Rules,Setting,ImageBanner, Blog , ImageBlog



# Register your models here.
class QuestionsInline(admin.TabularInline):
    model = Questions
    extra = 1
    min_num = 1
    fields = (
        "question",
        "answer",
    )
class RulesInline(admin.TabularInline):
    model = Rules
    min_num = 1
    extra = 1
    fields = (
        "rule",
    )
class ImageBannerInline(admin.TabularInline):
    model = ImageBanner
    extra = 1
    min_num = 3
    fields = (
        "image",
    )

@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = [
        "about",
        "phone",
        "id_tel",
        "footer",

    ]
    inlines = [RulesInline , QuestionsInline , ImageBannerInline]


class ImageBlogInline(admin.TabularInline):
    model = ImageBlog
    extra = 1
    min_num = 1
    max_num = 5
    fields = (
        "image",
    )

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "text",
        "author",
        "created",
        "updated",

    ]
    inlines = [ImageBlogInline]