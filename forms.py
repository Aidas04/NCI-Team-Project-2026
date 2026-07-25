# Edited by:
# Ionut Ciobanu
#

from allauth.account.forms import LoginForm, SignupForm
from django import forms

# Helper function to apply Bootstrap styling to form fields
def _style_auth_field(field, placeholder):
    # Apply Bootstrap form-control styling and placeholder text to form fields
    field.widget.attrs.update({
        "class": "form-control rounded-3 p-2",
        "placeholder": placeholder,
    })


# Custom login form extending allauth's LoginForm with Bootstrap styling
class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Style login field with Bootstrap classes and placeholder
        _style_auth_field(self.fields["login"], "Username or email")
        # Style password field with Bootstrap classes and placeholder
        _style_auth_field(self.fields["password"], "Password")


# Custom signup form extending allauth's SignupForm with mandatory first_name, last_name, email fields
class CustomSignupForm(SignupForm):
    # Add mandatory first_name and last_name fields to signup form
    first_name = forms.CharField(max_length=150, label="First name")
    last_name = forms.CharField(max_length=150, label="Last name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make first_name and last_name fields mandatory
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        # Ensure email is also mandatory for registration
        if "email" in self.fields:
            self.fields["email"].required = True

        # Define placeholder text for all signup form fields
        placeholders = {
            "first_name": "First name",
            "last_name": "Last name",
            "username": "Username",
            "email": "Email address",
            "password1": "Password",
            "password2": "Confirm password",
        }
        # Apply Bootstrap styling and placeholders to all fields
        for field_name, placeholder in placeholders.items():
            if field_name in self.fields:
                _style_auth_field(self.fields[field_name], placeholder)

    def save(self, request):
        # Save user after signup and persist first_name and last_name to database
        user = super().save(request)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        # Track which fields to update for efficient database query
        fields_to_update = ["first_name", "last_name"]
        # Also update email if provided
        if "email" in self.cleaned_data:
            user.email = self.cleaned_data["email"]
            fields_to_update.append("email")
        # Save only the updated fields to the database
        user.save(update_fields=fields_to_update)
        return user
