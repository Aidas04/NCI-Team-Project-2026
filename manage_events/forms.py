from django import forms
from home.models import Event


# form for organisers to create new events
# we also ask for password here so we can check its really them
class CreateEventForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Confirm your password")

    class Meta:
        model = Event
        fields = ['title', 'sport_type', 'location', 'date', 'start_time', 'capacity', 'price']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
        }