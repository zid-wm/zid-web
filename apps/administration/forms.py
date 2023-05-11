from django import forms

from apps.user.models import RATING_INTS


class SendEmailForm(forms.Form):
    subject = forms.CharField(
        label='Subject',
        widget=forms.TextInput(
            attrs={'class': 'form-control'})
    )
    sender_name = forms.CharField(
        label='Your Name',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}),
        initial=''
    )
    reply_email = forms.CharField(
        label='\"Reply To\" Email',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}),
        initial=''
    )
    ratings = forms.MultipleChoiceField(
        label='Included Ratings',
        widget=forms.SelectMultiple(
            attrs={'class': 'form-control'}
        ),
        choices=(),
        required=False
    )
    controllers = forms.MultipleChoiceField(
        label='Included Controllers',
        widget=forms.SelectMultiple(
            attrs={'class': 'form-control'}
        ),
        choices=(
            ('HC', 'Home Controllers'),
            ('TRAIN', 'Home Training Staff (Ignores Ratings)'),
            ('VC', 'Visiting Controllers')
        )
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control'}
        )
    )

    def __init__(self, request, *args, **kwargs):
        super(SendEmailForm, self).__init__(*args, **kwargs)
        self.fields['ratings'].choices = ((key, key) for key, value in RATING_INTS.items())
        self.fields['sender_name'].initial = request.user_obj.full_name
        self.fields['reply_email'].initial = request.user_obj.email


class StaffCommentForm(forms.Form):
    subject = forms.CharField(
        label='Controller',
        disabled=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    notes = forms.CharField(
        label='Notes',
        widget=forms.Textarea(attrs={
            'class': 'form-control'
        })
    )

    def __init__(self, subject, *args, **kwargs):
        super(StaffCommentForm, self).__init__(*args, **kwargs)
        self.fields['subject'].initial = subject
