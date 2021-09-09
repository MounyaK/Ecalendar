from datetime import datetime, timedelta
from calendar import HTMLCalendar
from django.conf import settings
from .models import Event, Room

import requests


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):

        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, events):
        events_per_day = events.filter(day__day=day)
        d = ''
        for event in events_per_day:
            d += f'<div class="card" style="width:100%;margin: 0 auto;text-align:center"><div class="card-body">{event}</div></div>'

        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):
        events = Event.objects.filter(day__year=self.year, day__month=self.month)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal


CURRENT_ROOM = Room.objects.first()


# Auth to API
def authenticate():
    api_route = settings.API_URL + "auth/login"
    data = {"email": CURRENT_ROOM.get_email, "password": CURRENT_ROOM.get_password}

    response = requests.post(api_route, data)
    if response.ok:
        headers = {"Authorization": "Bearer %s" % response.json()['access_token']}
        return headers
    else:
        return response.status_code
