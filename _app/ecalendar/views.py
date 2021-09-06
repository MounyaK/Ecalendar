import calendar
import json

from datetime import datetime, date, timedelta
import requests
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe

from .forms import EventForm
from .models import *
from .utils import Calendar, authenticate
from django.conf import settings

CURRENT_ROOM = Room.objects.first()


class CalendarView(generic.ListView):
    model = Event
    template_name = 'cal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        get_events()
        print("c_r =" + CURRENT_ROOM.get_title)

        # initiate calendar at the date given from url
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)

        # Contexts
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['event'] = event(self.request)
        context['rooms'] = Room.objects.all()
        context['current_room'] = CURRENT_ROOM

        return context


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


# event(request, event_id=None):

def event(request):
    api_route = settings.API_URL + "reservation/new"
    form = EventForm(request.POST or None)

    if request.POST and form.is_valid():

        # formatting
        form.cleaned_data['user_id'] = CURRENT_ROOM.get_userid
        form.cleaned_data['salle_id'] = CURRENT_ROOM.get_id
        form.cleaned_data['evenement'] = form.cleaned_data.pop('title')

        data = form.cleaned_data

        if verify_ok(request, form.cleaned_data['day'], form.cleaned_data['start_time'], form.cleaned_data['end_time']):
            headers = authenticate()
            response = requests.post(api_route, data=data, headers=headers)
            print(response.status_code)
            print(response.text)
            print(data)
            if response.ok:
                messages.success(request, 'Votre Demande sera traitée')
                return HttpResponseRedirect(reverse('ecalendar:calendar'))
            else:
                messages.error(request, 'une erreur est survenue')

    return render(request, 'cal/event.html', {'form': form})


def verify_ok(request, day, start, end):
    api_route = settings.API_URL + "salle/status"
    data = {'salle': CURRENT_ROOM.get_title, 'day': day, 'start': start, 'end': end}

    headers = authenticate()
    response = requests.post(api_route, data=data, headers=headers)

    if response.ok:
        messages.warning(request, 'Salle libre')
    else:
        messages.warning(request, 'salle occupée')
    return response.ok


# def set_room(room):
#     global CURRENT_ROOM
#     CURRENT_ROOM = room


def get_events():
    Event.objects.all().delete()

    api_route = settings.API_URL + "reservation/all?user="+str(CURRENT_ROOM.get_userid)
    headers = authenticate()
    response = requests.get(api_route, headers=headers)

    # save data in database
    data = response.json()['data']
    for e in data:
        if e['etat'] == "accepted":
            events = Event(id=e['id'],
                           title=e['evenement'],
                           day=e['day'],
                           start_time=e['start_time'],
                           end_time=e['end_time'],
                           user_id=e['user_id'],
                           disposition_id=e['disposition_id'],
                           salle_id=e['salle_id'],
                           nbre_siege=e['nbre_siege']
                           )
            events.save()