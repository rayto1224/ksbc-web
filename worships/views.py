from django.shortcuts import render
from django.http import JsonResponse
from .models import WorshipSermon

def worships_page(request):
    sermons = WorshipSermon.objects.all()

    years = WorshipSermon.objects.dates(
    'sermon_date',
    'year',
    order='DESC'
)
    speaker_names = (
        WorshipSermon.objects
        .values_list('speaker_name', flat=True)
        .distinct()
    )

    context = {
        'sermons': sermons,
        'years': years,
        'speaker_names': speaker_names,
    }
    return render(request, 'worships/worship.html', context)


def sermons_api(request):
    year = request.GET.get('year')
    speaker_name = request.GET.get('speaker_name')

    sermons = WorshipSermon.objects.all()

    if year:
        sermons = sermons.filter(sermon_date__year=year)

    if speaker_name:
        sermons = sermons.filter(speaker_name=speaker_name)

    data = {
        'sermons': [
            {
                'sermon_date': s.sermon_date.strftime('%Y-%m-%d'),
                'sermon_title': s.sermon_title,
                'speaker_name': s.speaker_name,
                'youtube_link': s.youtube_link,
            }
            for s in sermons
        ]
    }

    return JsonResponse(data)
