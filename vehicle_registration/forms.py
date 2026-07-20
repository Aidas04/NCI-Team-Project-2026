from django import forms
from .models import Vehicle

class VehicleRegistrationForm(forms.ModelForm):

    class Meta:
        model = Vehicle
        
        fields = [
            "registration_plate",
            "make",
            "model"
        ]

        widgets = {
            "registration_plate": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: 241-D-123456"
                }
            ),
            "make": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Toyota"
                }
            ),
            "model": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Corolla"
                }
            ),
        }