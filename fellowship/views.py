from .models import FellowshipEvent
from django.shortcuts import render


def fellowship_page(request):
    events = FellowshipEvent.objects.all().order_by("sort_order", "title")
    return render(request, "fellowship/fellowship.html", {"events": events})
