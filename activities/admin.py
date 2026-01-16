# events/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Event, EventParticipant


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'is_active',
        'start_date',
        'appl_deadline',
        'is_featured_badge',
        'is_free',
        'display_price',
        'quota_status',
        'is_expired',
        'created_at',
    )
    list_filter = (
        'is_featured',
        'is_free',
        'is_active',
        'is_announcement',
        'unlimited_quota',
        'start_date',
        'appl_deadline',
    )
    search_fields = ('title', 'description', 'location')
    list_editable = ('is_active',)
    list_per_page = 20
    date_hierarchy = 'start_date'
    ordering = ('-event_id',)

    fieldsets = (
        ('Basic Info', {
            'fields': (
                'title',
                'description',
                'location',
                'start_date',
                'appl_deadline',
                'poster',
            )
        }),
        ('Pricing & Quota', {
            'fields': (
                ('is_free', 'fee_amount', 'fee_currency'),
                'early_bird_fee',
                ('unlimited_quota', 'quota_left'),
            )
        }),
        ('Visibility & Type', {
            'fields': (
                'is_featured',
                'is_announcement',
            )
        }),
    )

    readonly_fields = ('event_id', 'created_at')   # if you add created_at later

    def is_featured_badge(self, obj):
        return format_html(
            '<span style="background:#ffcc00; color:black; padding:4px 8px; border-radius:4px;">Featured</span>'
            if obj.is_featured else '-'
        )
    is_featured_badge.short_description = "Featured"

    def quota_status(self, obj):
        if obj.unlimited_quota:
            return format_html('<span style="color:#28a745;">Unlimited</span>')
        if obj.quota_full:
            return format_html('<strong style="color:#dc3545;">FULL ({})</strong>', obj.quota_left)
        return f"{obj.quota_left} left"
    quota_status.short_description = "Quota"

    def is_expired(self, obj):
        return format_html(
            '<span style="color:#dc3545;">Expired</span>'
            if obj.is_expired else
            '<span style="color:#28a745;">Open</span>'
        )
    is_expired.boolean = False
    is_expired.short_description = "Status"


@admin.register(EventParticipant)
class EventParticipantAdmin(admin.ModelAdmin):
    list_display = (
        'event_title',
        'full_name_or_email',
        'email',
        'is_member',
        'registered_at',
        'registration_status_colored',
        'withdrawal_date',
    )
    list_filter = (
        'event',
        'registered_at',
        'withdrawal_date',
        'event__is_featured',
    )
    search_fields = (
        'email',
        'full_name',
        'event__title',
        'notes',
    )
    date_hierarchy = 'registered_at'
    list_per_page = 25
    ordering = ('-registered_at',)

    raw_id_fields = ('user', 'event')   # better for large numbers of users/events

    fieldsets = (
        (None, {
            'fields': ('event', 'email', 'user', 'full_name')
        }),
        ('Status & Metadata', {
            'fields': ('registered_at', 'withdrawal_date', 'notes'),
        }),
    )

    readonly_fields = ('registered_at',)

    def event_title(self, obj):
        return obj.event.title
    event_title.short_description = "Event"
    event_title.admin_order_field = 'event__title'

    def full_name_or_email(self, obj):
        return obj.full_name or obj.email
    full_name_or_email.short_description = "Name / Email"
    full_name_or_email.admin_order_field = 'full_name'

    def is_member(self, obj):
        return bool(obj.user)
    is_member.boolean = True
    is_member.short_description = "Member"

    def registration_status_colored(self, obj):
        status = obj.registration_status
        color = {
            "Accepted": "#28a745",
            "Withdrawn": "#6c757d",
            "Event ended": "#6c757d",
            "Rejected": "#dc3545",
        }.get(status, "#6c757d")
        return format_html('<span style="color:{};">{}</span>', color, status)
    registration_status_colored.short_description = "Status"
