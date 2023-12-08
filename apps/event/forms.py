from django import forms

from apps.event.models import Event


class EventForm(forms.Form):
    name = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    banner = forms.FileField(widget=forms.FileInput(
        attrs={'class': 'form-control'}), required=False)
    start = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control',
                'id': 'startDateTimePickerInput',
                'data-td-target': '#startDateTimePicker'
            }
        )
    )
    end = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control',
                'id': 'endDateTimePickerInput',
                'data-td-target': '#endDateTimePicker'
            }
        )
    )
    host = forms.CharField(max_length=16, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    event_signup_type = forms.ChoiceField(
        widget=forms.RadioSelect(
            attrs={
                'class': 'btn-check'
            }
        ),
        choices=Event.EVENT_SIGNUP_TYPE_CHOICES,
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}))


class AddPositionForm(forms.Form):
    callsign = forms.CharField(
        max_length=16, widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Callsign'
        }))
