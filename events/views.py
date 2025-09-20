from django.shortcuts import render
from .models import Event
from urllib.parse import urlencode
from django.utils.timezone import make_aware
from datetime import timezone

# Create your views here.

def index(request):
    events = Event.objects.all().order_by("start_time")
    
    for event in events:
        # A problem occured where the time from the website's event would be different from the time imported
        # into Google Calendar when you click "Add to Google Calendar". The code below corrects the timezones if different.
        start = event.start_time
        end = event.end_time

        # Make aware if naive
        if start.tzinfo is None:
            start = make_aware(start)
        if end.tzinfo is None:
            end = make_aware(end)
        
        # Convert to UTC
        start_utc = start.astimezone(timezone.utc)
        end_utc = end.astimezone(timezone.utc)

        # Build Google Calendar URL
        params = {
            "action": "TEMPLATE",
            "text": event.title,
            "dates": f"{start_utc.strftime('%Y%m%dT%H%M%SZ')}/{end_utc.strftime('%Y%m%dT%H%M%SZ')}",
            "details": event.description,
            "location": event.location,
        }
        event.google_calendar_url = "https://calendar.google.com/calendar/render?" + urlencode(params)
    
    return render(request, "events/index.html", {"events": events})