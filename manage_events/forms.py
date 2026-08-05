from datetime import date
from django import forms
from home.models import Event
from forms import _style_auth_field  # reusing the same helper the login/signup forms use


# these are the only game formats we allow people to pick from
GAME_FORMAT_CHOICES = [
    ("1v1 Basketball Tournament", "1v1 Basketball Tournament"),
    ("2v2 Basketball Tournament", "2v2 Basketball Tournament"),
    ("3v3 Basketball Tournament", "3v3 Basketball Tournament"),
    ("4v4 Basketball Tournament", "4v4 Basketball Tournament"),
    ("5v5 Basketball Tournament", "5v5 Basketball Tournament"),
    ("6v6 Basketball Tournament", "6v6 Basketball Tournament"),
]

# 15 locations around dublin, just picked well known areas/courts
DUBLIN_LOCATION_CHOICES = [
    ("Phoenix Park Courts", "Phoenix Park Courts"),
    ("Fairview Park", "Fairview Park"),
    ("Herbert Park", "Herbert Park"),
    ("St Anne's Park, Raheny", "St Anne's Park, Raheny"),
    ("Bushy Park, Terenure", "Bushy Park, Terenure"),
    ("Sean Moore Park, Ringsend", "Sean Moore Park, Ringsend"),
    ("Poppintree Park, Ballymun", "Poppintree Park, Ballymun"),
    ("Tymon Park, Tallaght", "Tymon Park, Tallaght"),
    ("Marlay Park, Rathfarnham", "Marlay Park, Rathfarnham"),
    ("Griffith Park, Drumcondra", "Griffith Park, Drumcondra"),
    ("Clontarf Sports and Leisure Centre", "Clontarf Sports and Leisure Centre"),
    ("UCD Sports Centre, Belfield", "UCD Sports Centre, Belfield"),
    ("DCU Sports Complex, Glasnevin", "DCU Sports Complex, Glasnevin"),
    ("National Basketball Arena, Tallaght", "National Basketball Arena, Tallaght"),
    ("Irishtown Stadium, Ringsend", "Irishtown Stadium, Ringsend"),
]

# form for organisers to create new events
class CreateEventForm(forms.ModelForm):
    # dropdown instead of free text, so title is always one of our approved formats
    title = forms.ChoiceField(choices=GAME_FORMAT_CHOICES, label="Event Title")
    # dropdown instead of free text, so location is always one of our approved spots
    location = forms.ChoiceField(choices=DUBLIN_LOCATION_CHOICES, label="Location")
    # capacity capped between 2 and 12 players, so it matches the model validators
    capacity = forms.IntegerField(min_value=2, max_value=12, label="Max Players")
    password = forms.CharField(widget=forms.PasswordInput, label="Confirm your password")

    class Meta:
        model = Event
        # sport_type left out on purpose, its always basketball so no need to ask
        fields = ['title', 'location', 'date', 'start_time', 'capacity', 'price']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'price': 'Price (EUR)',
            'password': 'Your account password',
        }
        for field_name, placeholder in placeholders.items():
            if field_name in self.fields:
                _style_auth_field(self.fields[field_name], placeholder)
        # dropdowns and date/time inputs also get the same rounded bootstrap look
        for field_name in ['title', 'location', 'date', 'start_time', 'capacity']:
            self.fields[field_name].widget.attrs.update({"class": "form-control rounded-3 p-2"})

    def clean_date(self):
        # stops anyone creating an event that already happened in the past
        chosen_date = self.cleaned_data.get("date")
        if chosen_date and chosen_date < date.today():
            raise forms.ValidationError("Event date must be in the future, you cant book the past!")
        return chosen_date