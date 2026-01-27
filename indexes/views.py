# indexes/views.py - 簡化版
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Ministry, Prayer  # 只導入這兩個！
from activities.models import Event


def home_page(request):
    """
    簡化版首頁 - 只顯示事工動態和代禱事項
    """
    # 1. 獲取事工動態
    recent_ministries = Ministry.objects.filter(is_active=True).order_by(
        "-activity_date"
    )[:5]

    # 2. 獲取代禱事項
    recent_prayers = Prayer.objects.filter(is_active=True).order_by(
        "-is_urgent", "-display_date"
    )[:]

    # 3. 獲取即將到來的活動（可選）
    today = timezone.now().date()
    events = Event.objects.filter(is_active=True, start_date__gte=today).order_by(
        "start_date"
    )[:3]

    context = {
        "recent_ministries": recent_ministries,
        "recent_prayers": recent_prayers,
        "events": events,  # 可選，如果您還想顯示活動
        "page_title": "嘉盛浸信會",
    }

    return render(request, "indexes/home.html", context)


def test(request):
    return render(request, "indexes/test.html")


def ministry_details(request, ministry_id):
    ministry = get_object_or_404(Ministry, pk=ministry_id)
    return render(request, "indexes/ministries.html", {"ministry": ministry})


def recent_ministries(request):
    pass
