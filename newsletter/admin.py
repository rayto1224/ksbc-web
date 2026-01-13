from django.contrib import admin
from .models import Newsletter
# Register your models here.

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'published_date',
        'is_published',
        'file_link',
        'created_at'
    )
    
    list_filter = ('is_published', 'published_date')
    search_fields = ('title', 'description')
    date_hierarchy = 'published_date'
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'published_date', 'is_published')
        }),
        ('Content', {
            'fields': ('pdf_file', 'description')
        }),
    )
    
    def file_link(self, obj):
        if obj.pdf_file:
            return f'<a href="{obj.pdf_file.url}" target="_blank">view PDF</a>'
        return "-"
    file_link.short_description = "PDF"
    file_link.allow_tags = True