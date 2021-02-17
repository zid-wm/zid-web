from django import forms
from apps.user.models import User
from apps.training.models import SESSION_LOCATIONS, OTS_STATUSES, PROGRESS_CHOICES


class TrainingTicketForm(forms.Form):
    student = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        choices=('', '')
    )

    session_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'placeholder': 'YYYY-MM-DD HH:MM'
        }),
        label='Session Date and Time (UTC)'
    )

    session_duration = forms.DurationField(
        widget=forms.TimeInput(attrs={
            'class': 'form-control',
            'placeholder': 'HH:MM'
        })
    )

    position = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    movements = forms.IntegerField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        label='Number of Movements'
    )

    score = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        choices=('', ''),
        label='Session Progress'
    )

    location = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        choices=('', ''),
        label='Session Location'
    )

    ots_status = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        choices=('', ''),
        label='OTS Status'
    )

    solo_granted = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': 'form-control'
        }),
        required=False
    )

    notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control'
        })
    )

    def __init__(self, *args, **kwargs):
        super(TrainingTicketForm, self).__init__(*args, **kwargs)

        user_items = User.objects.filter(
            main_role__in=['HC', 'VC']
        ).order_by('last_name')
        self.fields['student'].choices = (
            (u.cid, f'{u.first_name} {u.last_name}')
            for u in user_items
        )

        self.fields['score'].choices = PROGRESS_CHOICES
        self.fields['location'].choices = SESSION_LOCATIONS
        self.fields['ots_status'].choices = OTS_STATUSES
