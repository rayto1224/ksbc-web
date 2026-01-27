# indexes/admin.py - 簡化版
from django.contrib import admin
from django.utils.html import format_html
from .models import Ministry, Prayer  # 只導入這兩個！


class MinistryAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "activity_date",
        "location",
        "is_active",
        "display_order",
        "display_image",
    ]
    list_editable = ["is_active", "display_order", "activity_date"]
    list_filter = ["is_active", "activity_date"]
    search_fields = ["title", "description", "location"]

    fieldsets = (
        ("基本信息", {"fields": ("title", "description", "activity_date", "location")}),
        ("顯示控制", {"fields": ("is_active", "display_order")}),
        ("圖片", {"fields": ("image",), "description": "上傳活動照片（可選）"}),
    )

    def display_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover;" />',
                obj.image.url,
            )
        return "無圖片"

    display_image.short_description = "圖片"


class PrayerAdmin(admin.ModelAdmin):
    list_display = ["title", "display_date", "is_urgent", "is_active"]
    list_editable = ["is_urgent", "is_active", "display_date"]
    list_filter = ["is_urgent", "is_active"]
    search_fields = ["title", "content"]

    fieldsets = (
        ("代禱信息", {"fields": ("title", "content", "is_urgent", "is_active")}),
        ("時間設置", {"fields": ("display_date",), "description": "設定顯示日期"}),
    )

    admin.site.register(Ministry)
    admin.site.register(Prayer)
