
from django.contrib import admin
from .models import WorshipSermon

@admin.register(WorshipSermon)
class WorshipSermonAdmin(admin.ModelAdmin):
    list_display = ('sermon_date','sermon_title', 'speaker_name','youtube_link')
    list_filter = ('sermon_date', 'speaker_name')
    search_fields = ('sermon_title', 'speaker_name')
    ordering = ('-sermon_date',)
    date_hierarchy = 'sermon_date'
    
    fields = ('sermon_date','sermon_title', 'speaker_name', 'youtube_link')
