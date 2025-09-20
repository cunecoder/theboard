from datetime import date, timedelta
from urllib.parse import urlencode
from django.utils.timezone import make_aware, timezone
from collections import defaultdict
from .models import Event
from django.shortcuts import render

def index(request):
    events = Event.objects.all().order_by("start_time")
    
    for event in events:
        start = event.start_time
        end = event.end_time

        if start.tzinfo is None:
            start = make_aware(start)
        if end.tzinfo is None:
            end = make_aware(end)

        start_utc = start.astimezone(timezone.utc)
        end_utc = end.astimezone(timezone.utc)

        params = {
            "action": "TEMPLATE",
            "text": event.title,
            "dates": f"{start_utc.strftime('%Y%m%dT%H%M%SZ')}/{end_utc.strftime('%Y%m%dT%H%M%SZ')}",
            "details": event.description,
            "location": event.location,
        }
        event.google_calendar_url = "https://calendar.google.com/calendar/render?" + urlencode(params)

    today = date.today()
    date_range = [today + timedelta(days=i) for i in range(-3, 4)]

    return render(request, "events/index.html", {
        "events": events,
        "date_range": date_range,
        "today": today,
    })