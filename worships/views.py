from django.shortcuts import render
from django.http import JsonResponse
from .models import WorshipSermon
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def get_sermons(request):
    """API endpoint for AJAX filtering"""
    year = request.GET.get('year', '')
    
    sermons = WorshipSermon.objects.all().order_by('-sermon_date')
    
    if year:
        try:
            # Convert year to integer and filter
            year_int = int(year)
            sermons = sermons.filter(sermon_date__year=year_int)
        except ValueError:
            # If year is not a valid integer, return empty
            pass
    
    data = [
        {
            'id': sermon.id,
            'sermon_date': sermon.sermon_date.strftime('%Y-%m-%d'),
            'sermon_title': sermon.sermon_title,
            'speaker_name': sermon.speaker_name,
            'youtube_link': sermon.youtube_link,
        }
        for sermon in sermons
    ]
    
    return JsonResponse({'sermons': data})

def sermon_list(request):
    """Main view for worship sermons page"""
    # Get all sermons ordered by date (newest first)
    sermons_list = WorshipSermon.objects.all().order_by('-sermon_date')
    
    # FIXED: Get years as integers, not date objects
    from django.db.models.functions import ExtractYear
    years = WorshipSermon.objects.annotate(
        year=ExtractYear('sermon_date')
    ).values_list('year', flat=True).distinct().order_by('-year')
    
    # Convert QuerySet to list
    years = list(years)
    
    # Pagination (optional - remove if not needed)
    paginator = Paginator(sermons_list, 10)  # 10 sermons per page
    page = request.GET.get('page')
    
    try:
        sermons = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        sermons = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page
        sermons = paginator.page(paginator.num_pages)
    
    context = {
        'sermons': sermons,  # Paginated sermons
        'years': years,      # List of integers like [2026, 2025, 2024]
    }
    return render(request, 'worships/worship.html', context)