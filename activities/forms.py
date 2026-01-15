from django import forms
from .models import EventParticipant

class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventParticipant
        fields = ['email', 'full_name', 'telephone']   # add more fields if needed

    def __init__(self, *args, event=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.event = event

        # Make email required
        self.fields['email'].required = True

        if self.event and self.event.is_free:
            self.fields['full_name'].help_text = "Optional for free events"

    def clean_email(self):
        email = self.cleaned_data['email']
        if EventParticipant.objects.filter(event=self.event, email=email).exists():
            raise forms.ValidationError("This email is already registered for this event.")
        return email
