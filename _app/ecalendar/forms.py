import requests
from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm, DateInput, ChoiceField, TextInput
from .models import Event
from .utils import authenticate


# Fetch list of dispositions array from API
def get_disposition():
    api_route = settings.API_URL + "preference/all"
    headers = authenticate()
    response = requests.get(api_route, headers=headers)
    if response.ok:
        return response.json()['data']


class EventForm(ModelForm):

    class Meta:
        model = Event
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
            'start_time': DateInput(attrs={'type': 'time'}, format='%H:%M'),
            'end_time': DateInput(attrs={'type': 'time'}, format='%H:%M'),
            'day': DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'title': TextInput(attrs={'name': 'evenement'})
        }
        exclude = ['salle_id', 'user_id', 'id']

        label = {
            'disposition_id': _('disposition'),
            'start_time': _('heure début'),
            'end_time': _('heure fin'),
            'day': _('date'),
        }

        # help_texts ={
        #     'title': _('Précisez le nom du demandeur entre parenthèses.'),
        # }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields['start_time'].input_formats = ('%H:%M',)
        self.fields['end_time'].input_formats = ('%H:%M',)
        self.fields['day'].input_formats = ('%Y-%m-%d',)
        self.fields['disposition_id'] = forms.ChoiceField(choices=[(d['id'], d['libelle']) for d in get_disposition()])


