from django import forms

from apps.feedback.models import SERVICE_LEVEL_CHOICES
from apps.user.models import User


class NewFeedbackForm(forms.Form):
    user_items = User.objects.filter(
        status=0
    ).order_by('last_name')

    user_choices = ((u.id, f'{u.first_name} {u.last_name}') for u in user_items)

    # TODO: Format fields such that they have more padding between them
    controller = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        choices=user_choices
    )

    position = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    service_level = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        choices=SERVICE_LEVEL_CHOICES
    )

    flight_callsign = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        max_length=16
    )

    pilot_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Optional'
        }),
        required=False,
        max_length=64
    )

    pilot_email = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Optional'
        }),
        required=False,
        max_length=255
    )

    pilot_cid = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Optional'
        }),
        max_length=16,
        required=False,
        label='Pilot VATSIM CID'
    )

    additional_comments = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Optional'
        }),
        required=False
    )


class ReviewFeedbackForm(forms.Form):
    staff_comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Optional'
        }),
        required=False,
        label='Staff Comment'
    )
