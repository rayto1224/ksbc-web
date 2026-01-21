from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render
from django.db.models import Sum, F
from django.utils import timezone
from .models import Event, EventParticipant, Donation


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


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'amount',
        'date',
        'created_at',
    )
    search_fields = (
        'user__username',
        'user__email',
        'notes',
    )
    list_filter = (
        'date',
        'created_at',
    )
    date_hierarchy = 'date'
    ordering = ('-date', '-created_at')
    raw_id_fields = ('user',)
    change_list_template = "activities/admin/donation_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('summary/', self.admin_site.admin_view(self.summary_view), name='donation_summary'),
        ]
        return custom_urls + urls

    def summary_view(self, request):
        # Calculate financial year for each donation and aggregate
        # Since logic is complex for FY, we can fetch all and process in python or use complex annotations.
        # Python processing is easier for 'Apr-Mar' year logic unless dataset is huge.
        
        donations = Donation.objects.select_related('user').order_by('user__username', '-date')
        
        # Structure: { (user, fy_string): {'total': 0.0, 'donations': []} }
        from collections import defaultdict
        # Helper to create default dict entry
        def default_entry():
            return {'total': 0.0, 'donations': []}
            
        data = defaultdict(default_entry)
        fy_totals = defaultdict(float)
        
        for d in donations:
            if d.date.month >= 4:
                fy = f"{d.date.year}-{d.date.year + 1}"
            else:
                fy = f"{d.date.year - 1}-{d.date.year}"
            
            key = (d.user, fy)
            data[key]['total'] += float(d.amount)
            data[key]['donations'].append(d)
            fy_totals[fy] += float(d.amount)
            
        # Convert to list for template
        summary_list = []
        for (user, fy), info in data.items():
            summary_list.append({
                'user': user,
                'fy': fy,
                'total': info['total'],
                'donations': info['donations']  # List of donation objects
            })
            
        # FY Totals list sorted by FY desc
        fy_summary_list = sorted(
            [{'fy': fy, 'total': total} for fy, total in fy_totals.items()],
            key=lambda x: x['fy'],
            reverse=True
        )

        # Prepare filter options (all available FYs)
        # Sort headers descending (e.g. 2025-2026, 2024-2025)
        all_fys = sorted(fy_totals.keys(), reverse=True)

        # Handle Filtering
        selected_fy = request.GET.get('fy')
        if selected_fy and selected_fy in all_fys:
            # Filter the lists
            summary_list = [item for item in summary_list if item['fy'] == selected_fy]
            fy_summary_list = [item for item in fy_summary_list if item['fy'] == selected_fy]

        context = dict(
           self.admin_site.each_context(request),
           summary_list=summary_list,
           fy_summary_list=fy_summary_list,
           all_fys=all_fys,
           selected_fy=selected_fy,
           title="Donation Summary (Financial Year)"
        )
        return render(request, "activities/admin/donation_summary.html", context)


