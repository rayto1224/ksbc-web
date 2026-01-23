# views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count
from .models import WorshipSermon

def worships_page(request):
    """Main page view - renders worship.html"""
    # Get distinct years for filter dropdown
    years = WorshipSermon.objects.dates('sermon_date', 'year', order='DESC')
    years_list = [date.year for date in years]
    
    # Get distinct speakers for filter dropdown
    speakers = WorshipSermon.objects.values_list('speaker_name', flat=True).distinct().order_by('speaker_name')
    
    # Get all sermons initially
    sermons = WorshipSermon.objects.all().order_by('-sermon_date')
    
    # Count total sermons
    total_sermons = sermons.count()
    
    context = {
        'sermons': sermons,
        'years': years_list,
        'speakers': speakers,
        'total_sermons': total_sermons,
    }
    return render(request, 'worships/worship.html', context)  # Note: worship.html

def sermons_api(request):
    """API endpoint for AJAX filtering"""
    # Get filter parameters
    year = request.GET.get('year')
    speaker = request.GET.get('speaker')
    
    # Start with all sermons
    sermons = WorshipSermon.objects.all().order_by('-sermon_date')
    
    # Apply filters
    if year:
        sermons = sermons.filter(sermon_date__year=year)
    if speaker:
        sermons = sermons.filter(speaker_name=speaker)
    
    # Prepare response data
    data = {
        'sermons': [
            {
                'id': sermon.id,
                'sermon_date': sermon.sermon_date.strftime('%Y-%m-%d'),
                'sermon_title': sermon.sermon_title,
                'speaker_name': sermon.speaker_name,
                'youtube_link': sermon.youtube_link,
            }
            for sermon in sermons
        ]
    }
    return JsonResponse(data)