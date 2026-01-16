from django.contrib import admin
from .models import FellowshipEvent


# Register your models here.
@admin.register(FellowshipEvent)
class FellowshipEventAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "date_text",
        "time_text",
        "location",
        "is_active",
        "sort_order",
        "updated_at",
    )
    list_filter = ("is_active",)
    search_fields = ("title", "location", "description")
    ordering = ("sort_order", "title")
    list_editable = ("is_active", "sort_order")
