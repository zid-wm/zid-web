from django import forms

from user.models import ENDORSEMENTS, RATING_INTS


class AddMavpForm(forms.Form):
    facility_short = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Facility Identifier'
    }))
    facility_long = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Facility Name'
    }))


class EditProfileForm(forms.Form):
    profile_pic = forms.FileField(widget=forms.FileInput(
        attrs={'class': 'form-control'}
    ), label='Profile Picture', required=False)
    biography = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control'}
    ), required=False)


class EditEndorsementForm(forms.Form):
    delivery = forms.ChoiceField(
        widget=forms.Select,
        choices=ENDORSEMENTS
    )
    ground = forms.ChoiceField(
        widget=forms.Select,
        choices=ENDORSEMENTS
    )
    tower = forms.ChoiceField(
        widget=forms.Select,
        choices=ENDORSEMENTS
    )
    approach = forms.ChoiceField(
        widget=forms.Select,
        choices=ENDORSEMENTS
    )
    center = forms.ChoiceField(
        widget=forms.Select,
        choices=ENDORSEMENTS
    )


class VisitingRequestForm(forms.Form):
    cid = forms.IntegerField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly'
        }),
        label='CID'
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly'
        })
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly'
        })
    )
    rating = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-control',
            'readonly': 'readonly'
        }),
        choices=(
            ('S1', 'S1'),
            ('S2', 'S2'),
            ('S3', 'S3'),
            ('C1', 'C1'),
            ('C3', 'C3'),
            ('SUP', 'SUP'),
            ('ADM', 'ADM'),
        )
    )
    facility = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly'
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control'
        }),
        label='Why do you want to visit ZID?'
    )
